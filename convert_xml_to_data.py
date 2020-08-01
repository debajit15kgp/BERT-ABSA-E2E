import xml.etree.ElementTree as ET
tree = ET.parse('/home/debajit15/train.xml')
root = tree.getroot()

for child in root:
	for grandchild in child:
		for t in grandchild:
			print(t.tag,t.attrib)