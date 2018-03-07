#!/usr/bin/python

import os

#opts = ['0','1','2','3','4','5','6', '7', 'm1']
opts = ['2']

dirn = '../pred_combine/results/bmp51_len12/pred_110030080_p_0.00E+00/'
for opt in opts:
	print '-'*20, opt, '-'*20
	os.system('./new_reg_adjust.py ../testfiles/bmp51_len12/bmp51_len12.test '+dirn+' '+opt+' w110030080_o'+opt)
