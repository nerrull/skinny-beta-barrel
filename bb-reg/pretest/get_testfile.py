#!/usr/bin/python

# Will Tian, Jul 20, 2015
# For a given pretest file, give the test file for the further analysis
# A pretest file contains several lines, each line corresponding to a pdb record
# A line in a pretest file is like:
# pdb start1 end1 start2 end2 start3 end3 ...
# The line is whitespace separated

# Warning: This script needs files (pdb.tmstrands and pdb.tmregs) produced by bbpipe to work properly

import sys
sys.dont_write_bytecode = True
import numpy as np
import os

if len(sys.argv) < 2:
	print 'For a given pretest file, give the test file for the further analysis'
	print 'Usage :'+sys.argv[0]+' <pretest_file>'
	print 'No pretest_file provided, using the default one "bmp51_len12.pretest"'
	sys.argv.append("bmp51_len12.pretest")

fn = sys.argv[1]
f = open(fn)
lines = f.readlines()
f.close()


name = fn[:fn.rfind('.')]
if not os.path.exists('../testfiles/'+name):
	os.mkdir('../testfiles/'+name)

testf = open('../testfiles/'+name+'/'+name+'.test','w')
iperif = open(name+'.peris','w')
iextraf = open(name+'.extras','w')
listf = open(name+'.list','w')

for line in lines:
	split = line.split()
	pdb = split[0]
	intervals = []
	for i in range(1, len(split), 2):
		intervals.append((int(split[i]), int(split[i+1])))

	print("intervales :  {}".format( intervals))
	tmstrands = np.loadtxt('../inputs/'+pdb+'/'+pdb+'.tmstrands').astype(int)
	tmregs = np.loadtxt('../inputs/'+pdb+'/'+pdb+'.tmregs').astype(int)
	print("tmregs :  {}".format( tmregs))


	strandn = len(tmregs)
	intervalregs = []

	testf.write(pdb+' '+str(strandn))
	iperif.write(pdb+' '+str(strandn))
	iextraf.write(pdb+' '+str(strandn))
	listf.write(pdb+'\n')

	for i in range(strandn):
		if i%2==0:
			iextra = intervals[i][1]
			iperi1 = intervals[i][0]
			iperi2 = intervals[(i+1)%strandn][1]
			speri1 = tmstrands[i][0]
			speri2 = tmstrands[(i+1)%strandn][1]
			reg = iperi1 - speri1 + iperi2 - speri2 + tmregs[i]
			testf.write( ' '+str(intervals[i][0])+' '+str(intervals[i][1])+' '+str(reg) )
		else:
			iextra = intervals[i][0]
			iperi1 = intervals[i][1]
			iperi2 = intervals[(i+1)%strandn][0]
			speri1 = tmstrands[i][1]
			speri2 = tmstrands[(i+1)%strandn][0]
			reg = speri1 - iperi1 + speri2 - iperi2 + tmregs[i]
			testf.write( ' '+str(intervals[i][1])+' '+str(intervals[i][0])+' '+str(reg) )
		intervalregs.append(reg)
		iperif.write(' '+str(iperi1))
		iextraf.write(' '+str(iextra))

	testf.write('\n')
	iperif.write('\n')
	iextraf.write('\n')

testf.close()
iperif.close()
iextraf.close()
listf.close()

print ''
print 'test file   <', '../testfiles/'+name+'/'+name+'.test', '>   created in folder   <', '../testfiles/'+name+'/', '>'
print ''
