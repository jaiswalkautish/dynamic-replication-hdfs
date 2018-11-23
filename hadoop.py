import subprocess
import os
import glob
import xml.etree.ElementTree as ET

tmplogs_path = "/home/jaiswalkautish/Sem6/Project/tmp/hadoop-yarn/staging"
input_path = '/home/jaiswalkautish/Sem6/Project/XML'
out_path_hot = '/home/jaiswalkautish/Sem6/Project/XML/hot.txt'
out_path_cold = '/home/jaiswalkautish/Sem6/Project/XML/cold.txt'
out_path = '/home/jaiswalkautish/Sem6/Project/XML/output.txt'
rep_path = '/home/jaiswalkautish/Sem6/Project/XML/replicationFactor.txt'
pop_path = '/home/jaiswalkautish/Sem6/Project/XML/popularityIndex.txt'
newrep_path = '/home/jaiswalkautish/Sem6/Project/XML/newReplicationFactor.txt'
newpop_path = '/home/jaiswalkautish/Sem6/Project/XML/newPopularityIndex.txt'
names = {}
popularityIndex = {}
replicationFactor = {}
total = 0

def getFileName(file):
	tree = ET.parse(file)
	root = tree.getroot()
	value = None
	for properties in root.findall('property'):
		name = properties.find('name').text
		value = properties.find('value').text
		if(name == 'mapreduce.input.fileinputformat.inputdir'):
			break
	return value

def setReplicationFactor(path, rf):
	result = subprocess.run(['hdfs', 'dfs', '-setrep', '-R', str(rf), path], stdout = subprocess.PIPE)

def updateReplicationFactor(filename):
	ip = open(filename, 'r+')
	temp = ip.read().splitlines()
	for line in temp:
		setReplicationFactor(line, replicationFactor[line])
	ip.close()

def maintainFilecount(value):
	global total
	if(value != None):
		value = value.split('9000')
		if value[1] not in names:
			names[value[1]] = 1;
		else:
			names[value[1]] += 1;
		total = total + 1

def loadRepPop():
	ip = open(rep_path, 'r+')
	temp = ip.read().splitlines()
	for line in temp:
		line = line.split(' ')
		replicationFactor[line[0]] = int(line[1])
	ip.close()
	ip = open(pop_path, 'r+')
	temp = ip.read().splitlines()
	for line in temp:
		line = line.split(' ')
		popularityIndex[line[0]] = float(line[1])
	ip.close()

def saveRepPop():
	op = open(newrep_path, 'w+')
	#print ("Filename\tReplicationFactor")
	for rep in replicationFactor:
		#print (rep, replicationFactor[rep])
		op.write(rep + " " + str(replicationFactor[rep]) + "\n");
	op.close()
	#print ("Filename\tPopularityIndex")
	op = open(newpop_path, 'w+')
	for pop in popularityIndex:
		#print (pop, popularityIndex[pop])
		op.write(pop + " " + str(popularityIndex[pop]) + "\n");
	op.close()

def updateRepPop():
	global total
	oph = open(out_path_hot, "w+")
	opc = open(out_path_cold, "w+")
	for name in names:
		newPopI = popularityIndex[name]*0.4 + 0.6*(names[name]/total)
		if(newPopI >= 0.3):
			if(replicationFactor[name] <= 10):
				replicationFactor[name] += 1
			oph.write(name+"\n")
		else:
			if(replicationFactor[name] > 1):
				replicationFactor[name] -= 1
			opc.write(name+"\n")
		popularityIndex[name] = newPopI;
	oph.close()
	opc.close()
	saveRepPop()

def run():
	print ("\n")
	print ('Phase 2, "Aggregating Log Files" done \nObtained Log Files:')
	for file in glob.glob(os.path.join(input_path, '*.xml')):
		print (file)
		value = getFileName(file)
		maintainFilecount(value)
	print("\n")
	print ("Filename\tInitial Replication Factor")
	printD(replicationFactor)
	print("\n")
	print ("Filename\tInitial Popularity Index")
	printD(popularityIndex)
	print ("\n")
	print ('Phase 3, "Obtaining Filenames and MapReduce counts" done')
	print ('Filenames\tMapreduce Counts')
	printD (names)
	print ("\n")
	op = open(out_path, "w+")
	updateRepPop()
	
	print ('Phase 4, "Updating Popularity Index" done')
	print ('Filename\tNew Popularity Index')
	printD (popularityIndex)
	print ("\n")
	
	print ('Phase 5, "Updating Replication Factor" done')
	print ('Filename\tUpdated Replication Factor')
	printD (replicationFactor)
	for name in names:
		op.write(name + " " + str(names[name]) + "\n")
	op.close()
	updateReplicationFactor(out_path_hot)
	updateReplicationFactor(out_path_cold)
	print ("\nCluster Updated Successfully :)")

def queryaddress(path):
	res = []
	result = subprocess.run(['ls', path], stdout = subprocess.PIPE)
	ans = result.stdout.decode('utf-8')
	if(len(ans) == 0):
		return res
	fin = ans.split('\n')
	for i in fin:
		ans1 = i.split(':')
		if(len(ans1) == 1):
			if(ans1[0] == path):
				return res
			if(ans1[0][-4:] == '.xml'):
				res.append(path+'/'+ans1[0])
			elif(ans1[0] == ''):
				continue
			else:
				path1 = path
				path = path + '/' +ans1[0]
				res = res + queryaddress(path)
				path = path1
	return res

#result = subprocess.run(['hadoop', 'dfs', '-copyToLocal', '/tmp', '/home/jaiswalkautish/Sem6/Project'], stdout = subprocess.PIPE)
#ans = queryaddress(tmplogs_path)
#for file in ans:
#	subprocess.run(['cp', file, input_path])

def printD(data):
	for i in data:
		print (i +"\t\t"+ str(data[i]))

loadRepPop()
run()