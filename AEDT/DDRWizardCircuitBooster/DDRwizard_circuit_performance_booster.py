import re

bitrate_dict = {
				'bps'	:	1,
				'kbps'	:	1e3,
				'Mbps'	:	1e6,
				'Gbps'	:	1e9
				}

def VariableWithUnit2Float(varname):
	var_with_units=oProject.GetVariableValue(varname)
	pat = re.compile('([\-]*\d+[.\d+]*[eE\+\-\d+]*[.\d+]*)(\w+)')
	if re.findall(pat,var_with_units) != []:
		varvalue, unit = re.findall(pat,var_with_units)[0]
		return float(varvalue)*bitrate_dict[unit]
	
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("SchematicEditor")
eye_srcs = [c for c in oEditor.GetAllComponents() if 'EYESOURCE' in c]
for eye_src in eye_srcs:
	oEditor.ChangeProperty(
		[
			"NAME:AllTabs",
			[
				"NAME:Bits",
				[
					"NAME:PropServers", 
					eye_src
				],
				[
					"NAME:ChangedProps",
					[
						"NAME:step_resp_num_ui",
						"Value:="		, "10"
					]
				]
			]
		])
	AddInfoMessage("step_resp_num_ui of {} changed to 10 to speed-up analysis.".format(eye_src.split(';')[1]))
oModule = oDesign.GetModule("SimSetup")
bitrate = VariableWithUnit2Float('$bitrate')
tstep = 1/(bitrate*32)
QE_analyses = [setup for setup in oModule.GetAllSolutionSetups() if 'QuickEye' in setup]

for QE in QE_analyses:
	oModule.EditQuickEyeAnalysis(QE, 
		[
			"NAME:SimSetup",
			"DataBlockID:="		, 28,
			"OptionName:="		, "(Default Options)",
			"AdditionalOptions:="	, "eye.tstep="+str(tstep),
			"AlterBlockName:="	, "",
			"FilterText:="		, "",
			"AnalysisEnabled:="	, 1,
			"HasTDRComp:="		, 0,
			[
				"NAME:OutputQuantities"
			],
			[
				"NAME:NoiseOutputQuantities"
			],
			"Name:="		, QE,
			"QuickEyeAnalysis:="	, [False,"0",False,"0","",True,False]
		])
	AddInfoMessage('"eye.tstep='+str(tstep)+'" added to '+QE+" additional options to speed-up analysis")