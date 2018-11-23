import os
import glob
import xml.etree.ElementTree as ET

input_path = '/home/jaiswalkautish/Files'
out_path = '/home/jaiswalkautish/Files/output.txt'

def getFileName(file):
	tree = ET.parse(file)
	root = tree.getroot()
	for country in root.findall('property'):
		name = country.find('name').text
		value = country.find('value').text
		if(name == 'mapreduce.input.fileinputformat.inputdir'):
			break
	return value

def run():
	names = {}
	for file in glob.glob(os.path.join(input_path, '*.xml')):
		value = getFileName(file)
		if(value != None):
			value = value.split('9000')
			if value[1] not in names:
				names[value[1]] = 1;
			else:
				names[value[1]] += 1;
	op = open(out_path, "w+")
	for name in names:
		op.write(name + " " + str(names[name]) + "\n")
run()