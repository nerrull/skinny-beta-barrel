#!/usr/bin/python

import os
cwd = os.getcwd()

print ''
print 'beta barrel membrane protein register prediction'
print ''
print 'these scripts only support unix/linux system'
print 'please ignore "mkidr" warning when running'
print ''

print '  preparing input for register prediction...'
os.chdir(cwd+'/pretest/')
os.system('python get_bmp51_pretest.py > /dev/null')
os.system('python get_testfile.py')

os.chdir(cwd+'/testfiles/')
os.system('python separarte.py > /dev/null')

print '  computing sequence covariantion term from psicov results...'
os.chdir(cwd)
os.system('python all_reg_sc_scores.py')

print '  predicting registers...'
os.chdir(cwd+'/pred_combine/')
os.system('make')
os.system('python parallel_findbest.py > /dev/null')

print '  optimizing local register for better global shear...'
os.chdir(cwd+'/shear_adjustment/')
os.system('python get_all.py ')

print ''
