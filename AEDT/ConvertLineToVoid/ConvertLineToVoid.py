def DiffList(a,b):
    return [ia for ia in a if ia not in b]

oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.GetEditor("Layout")

ignoredProps = ['Type', 'Name', 'LockPosition', 'PlacementLayer', 'Net', 'LineWidth', 'Negative', 'BendType', 'StartCapType', 'EndCapType', 'TotalLength']

units = oEditor.GetActiveUnits()

linevoidGeometry = []
n = 0
sels = oEditor.GetSelections()

check_selections = True
if not sels:
	AddErrorMessage('No selections. Script will not proceed.')
	check_selections = False
elif 'poly' not in sels[0] and 'rect' not in sels[0]:
	AddErrorMessage('First selection need to be the owner polygon/rectangle of the void. Script will not proceed.')
	check_selections = False
else:
	OwnerPolygon = sels.pop(0)

if check_selections:
	for s in sels:
		sel_props = oEditor.GetProperties('BaseElementTab',s)
		if 'Type' in sel_props:
			if oEditor.GetPropertyValue('BaseElementTab',s,'Type') == 'line':
				layer = oEditor.GetPropertyValue('BaseElementTab',s,'PlacementLayer')
				lw = oEditor.GetPropertyValue('BaseElementTab',s,'LineWidth')
				line_pts = DiffList(sel_props,ignoredProps)
				for p in line_pts:
					coord = oEditor.GetPropertyValue('BaseElementTab',s,p).split(' ,')
					if len(coord) == 1:
						linevoidGeometry.append("x:=") 
						linevoidGeometry.append(coord[0])
						linevoidGeometry.append("y:=")
						linevoidGeometry.append('1E+200')
						n += 1
					elif len(coord) == 2:
						linevoidGeometry.append("x:=") 
						linevoidGeometry.append(coord[0]+units)
						linevoidGeometry.append("y:=")
						linevoidGeometry.append(coord[1]+units)
						n += 1

		linevoidGeometry_pre = [
					"Name:="		, "{} void".format(s),			
					"LayerName:="		, layer,			
					"lw:="			, lw,			
					"endstyle:="		, 0,			
					"StartCap:="		, 0,			
					"n:="			, n,			
					"U:="			, "meter"
				]            

		oEditor.CreateLineVoid(
			[
				"NAME:Contents",
				"owner:="		, OwnerPolygon,
				"line voidGeometry:=", linevoidGeometry_pre + linevoidGeometry + ["MR:=", "600mm"]
			])
		oEditor.Delete([s])
		linevoidGeometry = []
		n = 0

