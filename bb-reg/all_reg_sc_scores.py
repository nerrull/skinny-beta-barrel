#!/usr/bin/python
import os
import time


peris_file = 'pretest/bmp51_len12.peris'
pdb_list = 'pretest/bmp51_len12.list'
ec_raw_dir = 'sc.psicov'
weight_list = ['110 030 080']

output_dir0 = 'reg_sc_scores/bmp51_len12'




for weights in weight_list:
	os.system('python get_reg_sc_scores.py --peris_file {peris_file} --pdb_list {pdb_list} --output_dir {output_dir} --weights {weights} --ec_raw_dir {ec_raw_dir} --logp {logp} '.format( peris_file = peris_file, pdb_list = pdb_list, output_dir = output_dir0, weights = weights, ec_raw_dir = ec_raw_dir, logp=0))
