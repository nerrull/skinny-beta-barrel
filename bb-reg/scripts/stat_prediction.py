#### stat .pred file


import sys

if len(sys.argv)!=2:
	print 'Usage: '+argv[0]+' pred_file'
	sys.exit(0)


with open(sys.argv[1]) as f:
	lines = f.readlines()

strand_num = 0
none_num = 0
correct_num = 0
wrong_counts = {}

for line in lines:
	split = line.split()
	if not len(split) > 2:
		continue

	strand_num += 1
	true, pred, score = split[2], split[3], split[5]
	true = int(true)
	try:
		pred = int(pred)
	except:
		pred = None
		none_num += 1
		continue
	score = float(score)

	if pred == true:
		correct_num += 1
	else:
		miss = pred - true
		if miss in wrong_counts:
			wrong_counts[miss] += 1
		else:
			wrong_counts[miss] = 1


print '~'*20
print '## stats of', sys.argv[1]
print 'total strand num : ', strand_num
print 'no ec num : ', none_num
print 'effective strand num : ', strand_num-none_num
print 'correct num : ', correct_num
print 'total correct rate : ', float(correct_num)/strand_num
print 'effective correct rate : ', float(correct_num)/(strand_num-none_num)
#print 'wrong offset counts : '
#for k in sorted(wrong_counts.keys()):
#	print '  ', k, wrong_counts[k]
