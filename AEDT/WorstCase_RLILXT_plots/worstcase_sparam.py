input_file = r"Scripts\aapyAEDT\WorstCase_touchstone\Example.s96p" #r"D:\Scripts\aapyAEDT\WorstCase_touchstone\SSN.aedt"  # ''
driver_preffix = "U1"
receiver_preffix = "U7"

# +

import os
import re
import sys
from pathlib import Path
from ansys.aedt.core import Hfss3dLayout, Circuit
from ansys.aedt.core.visualization.advanced.touchstone_parser import \
    read_touchstone
# -

def check_input_file(inputfile):
    if os.path.exists(inputfile) or inputfile == '':
        if re.search('s\d+p',Path(inputfile).suffix):
            return 'Touchstone'
        elif Path(inputfile).suffix == '.ts':
            return 'Touchstone'
        elif Path(inputfile).suffix == '.aedt':
            return 'AEDT'
        elif inputfile == '':
            return 'Interactive'
        else:
            sys.exit('Unsupported input file format.')
    else:
        sys.exit('Input file does not exist.')

def check_preffix(preffix):
    if [p for p in data.port_names if preffix in p]:
        return True
    else:
        return False

def plot_expression(ports_duo,exp_category='S',exp_function='dB'):
    pnames = data.port_names
    return '{}({}({},{}))'.format(
                                    exp_function,
                                    exp_category,
                                    pnames[ports_duo[0]],
                                    pnames[ports_duo[1]]
                                 )

input_type = check_input_file(input_file)
if input_type == 'Touchstone':
    touchstone_path = input_file
    project_name = Path(input_file).stem + '_WorstCase_Check.aedt'
    tool = Circuit(
        project=os.path.join(os.path.dirname(input_file),project_name),
        version='2025.1'
        )
elif input_type == 'AEDT':
    tool = Hfss3dLayout(
        project=input_file,
        version="2025.1")
    touchstone_path = tool.export_touchstone()
elif input_type == 'Interactive':  
    tool = Hfss3dLayout()
    touchstone_path = tool.export_touchstone()

# ## Read the Touchstone file

if touchstone_path and os.path.exists(touchstone_path):
    data = read_touchstone(touchstone_path)
else:
    tool.odesktop.AddMessage('','',2,'Touchstone export failed! Script will stop.')
    tool.release_desktop(False,False)
    exit()


if input_type == 'Touchstone':
    tool.odesign.ImportData(
   	[
   		"NAME:NPortData",
   		"Name:="		, data.name,
   		"Description:="		, "",
   		"ImageFile:="		, "",
   		"SymbolPinConfiguration:=", 0,
   		["NAME:PortInfoBlk"],
   		["NAME:PortOrderBlk"],
   		"filename:="		, input_file,
   		"numberofports:="	, data.number_of_ports,
   		"sssfilename:="		, "",
   		"sssmodel:="		, False,
   		"PortNames:="		, data.port_names,
   		"domain:="		, "frequency",
   		"datamode:="		, "Link",
   		"devicename:="		, "",
   		"SolutionName:="	, data.name,
   		"displayformat:="	, "MagnitudePhase",
   		"datatype:="		, "SMatrix",
   		[],
   		[],
   		[],
   		"NoiseModelOption:="	, "External"
   	], "", False)
    setup_name = data.name + ' : ' + data.name
elif input_type == 'AEDT' or input_type == 'Interactive':
    setup_name = tool._app.nominal_sweep

# ## Demonstrate post-processing
#
# ### Plot using matplotlib serial channel metrics
#
# Get the curve plot by category. The following code shows how to plot lists of the return losses,
# insertion losses, next, and fext based on a few inputs and port names. Uncomment below if you want to plot

# data.plot_return_losses()
# data.plot_insertion_losses()
# data.plot_next_xtalk_losses(driver_preffix)
# data.plot_fext_xtalk_losses(tx_prefix=driver_preffix, rx_prefix=receiver_preffix)

# ### Plot all curves into AEDT 
# 
# This could be very long if number of curves is big. 
tool.post.create_report(
    expressions=[plot_expression(rl) for rl in data.get_return_loss_index()],
    plot_name='All RL',
    setup_sweep_name=setup_name,
    primary_sweep_variable="Freq"
    )
tool.post.create_report(
    expressions=[plot_expression(il) for il in data.get_insertion_loss_index()],
    plot_name='All IL',
    setup_sweep_name=setup_name,
    primary_sweep_variable="Freq"
    )
# tool.post.create_report(
#     expressions=[plot_expression(nx) for nx in data.get_next_xtalk_index(driver_preffix)],
#     plot_name='All NEXT',
#     setup_sweep_name=setup_name,
#     primary_sweep_variable="Freq"
#     )
# tool.post.create_report(
#     expressions=[plot_expression(fx) for fx in data.get_fext_xtalk_index_from_prefix(driver_preffix,receiver_preffix)],
#     plot_name='All FEXT',
#     setup_sweep_name=setup_name,
#     primary_sweep_variable="Freq"
#     )
#
# ## Identify worst cases and plot into AEDT
# 
# Return Losses
worst_rl, _ = data.get_worst_curve(
    worst_is_higher=True,
    curve_list=data.get_return_loss_index(),
    plot=False
)
tool.post.create_report(
    expressions=plot_expression(worst_rl),
    plot_name='Worst RL',
    setup_sweep_name=setup_name,
    primary_sweep_variable="Freq"
    )

# Insertion Losses
worst_il, _ = data.get_worst_curve(
    worst_is_higher=False,
    curve_list=data.get_insertion_loss_index(),
    plot=False
)
tool.post.create_report(
    expressions=plot_expression(worst_il),
    plot_name='Worst IL',
    setup_sweep_name=setup_name,
    primary_sweep_variable="Freq"
    )

# NEXT and FEXT
if check_preffix(driver_preffix) and check_preffix(receiver_preffix):
    worst_fext, _ = data.get_worst_curve(
        worst_is_higher=True,
        curve_list=data.get_fext_xtalk_index_from_prefix(tx_prefix=driver_preffix, rx_prefix=receiver_preffix),
        plot=False
    )
    worst_next, _ = data.get_worst_curve(
        worst_is_higher=True,
        curve_list=data.get_next_xtalk_index(driver_preffix),
        plot=False
    )
    
    tool.post.create_report(
        expressions=plot_expression(worst_fext),
        plot_name='Worst FEXT',
        setup_sweep_name=setup_name,
        primary_sweep_variable="Freq"
        )
    tool.post.create_report(
        expressions=plot_expression(worst_next),
        plot_name='Worst NEXT',
        setup_sweep_name=setup_name,
        primary_sweep_variable="Freq"
        )
else:
    tool.odesktop.AddMessage('','',1,"Driver or Receiver preffix not found. NEXT and FEXT won't be plotted.")


tool.release_desktop(False,False)