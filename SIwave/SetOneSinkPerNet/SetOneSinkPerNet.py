inputFile = r"D:\test\dummy_pkg_wo_src_snk.siw"

# =====================================================================================================================================
# =================================================== Code starts here: ===============================================================
# =====================================================================================================================================

import re

def Msg(message,msglvl=0):
    if "oDesktop" in globals():
        oDesktop.AddMessage('','',msglvl,message)
    elif "oDoc" in globals():
        if msglvl == 0:
            oDoc.ScrAddInfo(message)
        elif msglvl==1:
            oDoc.ScrAddWarning(message)
        elif msglvl==2:
            oDoc.ScrAddError(message)
    else:
        print(message)

with open(inputFile,'r') as fi:
    fi_txt = fi.read()

# set all pins to source
pat_src = re.compile('(  X \d+ \d+ \d+ \d+ [-]*\d+.\d+e[-\+]*\d+ [-]*\d+.\d+e[-\+]*\d+ [-]*\d+.\d+e[-\+]*\d+ \w+ \w+ \w+ )([F~]) ')
fo_txt = re.sub(pat_src,'\g<1>\\ ',fi_txt)

# get net id from each net
pat_nets = re.compile('B_NETS(.*?)E_NETS',re.DOTALL)
nets_txt = re.findall(pat_nets, fo_txt)
if nets_txt != []:
    nets_txt = nets_txt[0].strip()
    nets = {net.split()[0]:{'Net Name':net.split()[1]} for net in nets_txt.strip().split('\n  ')}

# get number of sources and sinks of original project
pat_geometry = re.compile('B_GEOMETRY(.*?)E_GEOMETRY',re.DOTALL)
geometry_txt = re.findall(pat_geometry, fo_txt)
if geometry_txt != []:
    geometry_lst = geometry_txt[0].strip().split('\n  ')
    for line in geometry_lst:
        if line[0] == 'X':
            line_objs = line.split()
            if line_objs[8] != '(NULL)':
                net_id = line_objs[1]
                refdes = line_objs[9]
                if 'Components' not in nets[net_id].keys():
                    nets[net_id]['Components']={}
                if 'Num Sources' not in nets[net_id].keys():
                    nets[net_id]['Num Sources']=0
                if 'Num Sinks' not in nets[net_id].keys():
                    nets[net_id]['Num Sinks']=0

                if refdes not in nets[net_id]['Components'].keys():
                    nets[net_id]['Components'][refdes]={}

                if '|' in line_objs[10]:
                    pin_number = line_objs[10].split('|')[0]
                else:
                    pin_number = line_objs[10]
                if pin_number not in nets[net_id]['Components'][refdes].keys():
                    nets[net_id]['Components'][refdes][pin_number]=''

                if line_objs[11] == '\\':
                    nets[net_id]['Components'][refdes][pin_number] = ['Source',line]
                    nets[net_id]['Num Sources'] += 1
                elif line_objs[11] == '~':
                    nets[net_id]['Components'][refdes][pin_number] = ['Sink',line]
                    nets[net_id]['Num Sinks'] += 1
                elif line_objs[11] == 'f':
                    nets[net_id]['Components'][refdes][pin_number] = ['Float',line]

# change sink to source if net contains more than one sink
for net in nets:
    if nets[net]['Num Sinks'] > 1:
        for comp in nets[net]['Components']:
            for pin in nets[net]['Components'][comp]:
                if nets[net]['Components'][comp][pin][0] == 'Sink':
                    tmp_line = nets[net]['Components'][comp][pin][1]
                    tmp_line_lst = tmp_line.split()
                    tmp_line_lst[11]='\\'
                    new_line = ' '.join(tmp_line_lst)
                    fo_txt=fo_txt.replace(tmp_line,new_line)
                    print('Pin {} of component {} was changed from {} to {}'.format(pin,comp,'Sink','Source'))
                    nets[net]['Num Sinks'] -= 1
                    break
            else:
                continue
            break

# change source to sink if net contains less than one sink
for net in nets:
    if nets[net]['Num Sinks'] < 1:
        for comp in nets[net]['Components']:
            for pin in nets[net]['Components'][comp]:
                if nets[net]['Components'][comp][pin][0] == 'Source':
                    tmp_line = nets[net]['Components'][comp][pin][1]
                    tmp_line_lst = tmp_line.split()
                    tmp_line_lst[11]='~'
                    new_line = ' '.join(tmp_line_lst)
                    fo_txt=fo_txt.replace(tmp_line,new_line)
                    print('Pin {} of component {} was changed from {} to {}'.format(pin,comp,'Source','Sink'))
                    break
            else:
                continue
            break

# write output file with suffix "_new"
with open(inputFile.replace('.siw','_new.siw'),'w') as fo:
    fo.write(fo_txt)
    Msg('{} created successfuly!'.format(fo.name)
                    
