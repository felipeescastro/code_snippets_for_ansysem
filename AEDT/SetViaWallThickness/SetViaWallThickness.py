ViaWallThickness = "100um"

# =================================================================
import re

units_dict = {
				'meter'	:	1,
				'm'		:	1,
				'cm'	:	1e-2,
				'mm'	:	1e-3,
				'um'	:	1e-6,
				'nm'	:	1e-9,
				'mil'	:	2.54e-5,
				'in'	:	0.254
				}
				
def ValueWithUnit2Float(valuewithunit):
	pat = re.compile('([\-]*\d+[.\d+]*[eE\+\-\d+]*[.\d+]*)(\w+)')
	if re.findall(pat,valuewithunit) != []:
		varvalue, unit = re.findall(pat,valuewithunit)[0]
		return float(varvalue)*units_dict[unit]

oProject = oDesktop.GetActiveProject()
oDefinitionManager = oProject.GetDefinitionManager()
oPadstackManager = oDefinitionManager.GetManager("Padstack")

for pdef in oPadstackManager.GetNames():
	pdef_data = oPadstackManager.GetData(pdef)
	oldHoleDiam = pdef_data[9][11][3][0]
	oldHoleDiam_num = ValueWithUnit2Float(oldHoleDiam)
	ViaWallThickness_num = ValueWithUnit2Float(ViaWallThickness)
	newHoleDiam_num = oldHoleDiam_num + 2*ViaWallThickness_num
	newViaPlating = (2*ViaWallThickness_num/newHoleDiam_num)*100
	pdef_data[9][11][3][0] = str(newHoleDiam_num)
	pdef_data[9][8] = str(newViaPlating)
	oPadstackManager.Edit(pdef, pdef_data)
	AddInfoMessage('Via Wall Thickness of {} changed to {}.'.format(pdef,ViaWallThickness))