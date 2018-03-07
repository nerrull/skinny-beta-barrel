#!/usr/bin/python
import os

cwd = os.getcwd()

print 'preparing input from register prediciton results...'
os.chdir(cwd+'/construction_inputs/')
os.system('bash process_all.sh')

os.chdir(cwd)

print 'constructing Ca atoms...'
os.system('python construct_ca_pdb.py')

print 'constructing backbone atoms from Ca atoms using BBQ algorithm...'
os.system('python construct_bb_pdb.py 2> /dev/null')

print 'constructing sidechains using Scwrl4...'
os.system('python construct_sc_pdb.py')

print 'cleaning tmp info to generate final structures...' 
os.system('python correct_index_and_trim.py')

#
# print 'computing rmsd...'
# os.system('python all_rmsd.py')
