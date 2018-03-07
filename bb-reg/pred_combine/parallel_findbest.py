#!/usr/bin/python


import sys
sys.dont_write_bytecode = True
sys.path.append('../scripts')
import cfg
import glob
import os 
import time


if len(sys.argv)<2:
	print 'Usage: '+sys.argv[0]+' <cfg_file>'
	print 'no cfg_file provided, using default "cfg/bmp51_len12.cfg"'
	sys.argv.append('cfg/bmp51_len12.cfg')



cfgdict = cfg.read_cfg(sys.argv[1])

score_folder = cfgdict['score_folder']
odds_folder = cfgdict['odds_folder']
test_folder = cfgdict['test_folder']

if '110030080' in score_folder:
	execprog = './exec/new_pred_reg_search_l1o_ecparam110030080.out'
	execprog = './exec/new_pred_reg_bestweight_ecparam110030080.out'
	execprog = './exec/new_pred_reg_bestscore_ecparam110030080.out'
elif '110020070' in score_folder:
	execprog = './exec/new_pred_reg_search_l1o_ecparam110020070.out'
	execprog = './exec/new_pred_reg_bestweight_ecparam110020070.out'
	execprog = './exec/new_pred_reg_bestscore_ecparam110020070.out'
elif '110010080' in score_folder:
	execprog = './exec/new_pred_reg_search_l1o_ecparam110010080.out'
	execprog = './exec/new_pred_reg_bestweight_ecparam110010080.out'
	execprog = './exec/new_pred_reg_bestscore_ecparam110010080.out'
else:
	execprog = './exec/new_pred_reg_search.out'
	pass

#execprog = './exec/new_pred_reg_bestscore_ecparam110030080.out'
#execprog = './exec/right_new_pred_reg_bestweight_ecparam110030080.out'
execprog = './exec/new_pred_reg_bestscore_ecparam110030080.out'

rdirn1 = test_folder[test_folder.rfind('testfiles')+10:]
rdirn1 = 'results/'+rdirn1
os.system('mkdir '+rdirn1)


for sfn in sorted(glob.glob(score_folder+'/*.ecs')):
	rdirn2 = sfn[sfn.rfind('/')+1:sfn.rfind('.')]
	rdirn = rdirn1+'/'+rdirn2
	os.system('mkdir '+rdirn)
	for tfn in sorted(glob.glob(test_folder+'/*.l??')):
		rfn = tfn[tfn.rfind('/')+1:]

		#qsubf = open('qtmpsub', 'w')
		#qsubf.write('#$ -S /bin/bash \n#$ -j y \n#$ -m be \n#$ -cwd \n#$ -N haha\n')
		#qsubf.write(execprog+' '+tfn+' '+sfn+' '+odds_folder+' > '+rdirn+'/'+rfn)
		#qsubf.close()
		#os.system('qsub qtmpsub')
		#time.sleep(0.3)

		print(execprog+' '+tfn+' '+sfn+' '+odds_folder+' > '+rdirn+'/'+rfn+' &')
		os.system(execprog+' '+tfn+' '+sfn+' '+odds_folder+' > '+rdirn+'/'+rfn +' &')
		#os.system(execprog+' '+tfn+' '+sfn+' '+odds_folder)
		#time.sleep(1)

#os.system('rm qtmpsub')


