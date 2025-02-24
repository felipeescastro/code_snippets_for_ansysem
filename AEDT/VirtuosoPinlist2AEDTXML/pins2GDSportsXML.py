pinlist_file = r"D:\Scripts\3DLayout\GDS2GDSCompXML\pinlist.out"
refLayer = "Ground" # Usually called "backplane" too

# ==============================================================================================================================================================

import re
import math
 
def convert_to_xml(input_string,pinnumber):
	regex = r'\"(\w+[<\[\{]*\d*[>\]\}]*)\s+\(\((-?\d+\.\d+)\s+(-?\d+\.\d+)\)\s+\((-?\d+\.\d+)\s+(-?\d+\.\d+)\)\)\s+\(\\\"(\w+)\\\"\s+\\\"(\w+)\\\"\)\"'

	match = re.match(regex, input_string)
	if match:
		name = match.group(1)
		x1 = float(match.group(2))
		y1 = float(match.group(3))
		x2 = float(match.group(4))
		y2 = float(match.group(5))
		x = math.floor((x1 + x2)*500.0)/1000.0
		y = math.floor((y1 + y2)*500.0)/1000.0
		layer1 = match.group(6)

		xml_string = f'<CircuitPortPt Name="Port_{name}_{pinnumber}" x1="{x}" y1="{y}" Layer1="{layer1}" x2="{x}" y2="{y}" Layer2="{refLayer}"/>'
		return xml_string
 
	return None

fileout = open(pinlist_file.replace('.out',".xml"), "w")

fo_txt = "<!-- To be copied inside of XML's <Boundaries> session -->\n"
with open(pinlist_file) as f:
	pinnumber=0
	for line in f:
		input_string = str(line)
		xml_output = convert_to_xml(input_string,pinnumber)
		pinnumber += 1
		fo_txt += "\t" + xml_output + "\n"

fileout.write(fo_txt)
fileout.close()