#!/usr/bin/python
import sys
sys.dont_write_bytecode = True
import glob

if len(sys.argv)<2:
	print 'Usage: '+sys.argv[0]+' <testfolder>'
	print 'no testfolder provided, using default "bmp51_len12"'
	sys.argv.append("bmp51_len12")


l01 = ['1bxw', '1qj8', '1p4t', '2f1t', '1thq', '2erv', '2lhf', '2mlh', '3dzm', '1qd6', '2f1c', '1k24', '1i78', '2wjr', '4pr7', 'unkn']
l02 = ['1t16', '1uyn', '1tly', '3aeh', '3bs0', '3dwo', '3fid', '3kvn', '4e1s']
l03 = ['2mpr', '1a0s', '2omf', '2por', '1prn', '1e54', '2o4v', '3vzt', '4k3c', '4k3b', '4c4v', '4n75', '3emn']
l04 = ['2qdz', '2ynk', '3rbh', '3syb', '3szv', '4c00', '4gey', '3emn']
l05 = ['1fep', '2fcp', '1kmo', '1nqe', '1xkw', '2vqi', '3csl', '3rfz', '3v8x', '4q35']

fn = glob.glob(sys.argv[1]+'/*.test')[0]
with open(fn) as f:
	lines = f.readlines()

fn = fn[:fn.rfind('.test')]
fl01 = open(fn+'.l01','w')
fl02 = open(fn+'.l02','w')
fl03 = open(fn+'.l03','w')
fl04 = open(fn+'.l04','w')
fl05 = open(fn+'.l05','w')

for line in lines:
	if line[:4] in l01:
		fl01.write(line)
	#elif line[:4] in l02:
	if line[:4] in l02:
		fl02.write(line)
	#elif line[:4] in l03:
	if line[:4] in l03:
		fl03.write(line)
	#elif line[:4] in l04:
	if line[:4] in l04:
		fl04.write(line)
	#elif line[:4] in l05:
	if line[:4] in l05:
		fl05.write(line)

fl01.close()
fl02.close()
fl03.close()
fl04.close()
fl05.close()

