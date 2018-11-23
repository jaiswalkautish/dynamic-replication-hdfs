import subprocess

def queryAddress(num):
	str = 'blk_' + num
	result = subprocess.run(['hdfs', 'fsck', '-blockId', str], stdout = subprocess.PIPE)
	ans = result.stdout.decode('utf-8')
	print(ans)
	s = 'Block belongs to: '
	fin = ans.split('\n')
	ans = ''
	for res in fin:
		if res.startswith(s):
			ans = res[len(s):]
	return ans

def setReplicationFactor(path):
	result = subprocess.run(['hdfs', 'dfs', '-setrep', '-R', '3', path], stdout = subprocess.PIPE)

def execute():
	ip = open('inp.txt', 'r+')
	op = open('out.txt', "w+")
	temp = ip.read().splitlines()
	for line in temp:
		print (temp)
		#ans = queryAddress(line)
		#setReplicationFactor(ans)
		#op.write(line + " " + ans + "\n")
	op.close()
	ip.close()
execute()