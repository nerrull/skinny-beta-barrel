import sys
sys.path.append('../scripts/')
import pdb_info


keepdicts = {
		'ca':['CA'],
		'bb':['C','N','CA','O'],
		'sc':[]
		}

info = pdb_info.read_pdb_info('../pdb_info.list')

for keeptype in keepdicts.keys():
	for pdb in info.keys():
		chain = info[pdb]['chain']
		with open('../inputs/'+pdb+'/'+pdb+'.pdb') as f:
			lines = f.readlines()

		with open('pdb_'+keeptype+'/'+pdb+'.'+keeptype+'.pdb','w') as f:
			for line in lines:
				if not line.startswith('ATOM'):
					continue
				if line[21]!=chain:
					continue
				# ignore if having alternative location
				if line[16]!=' ' and line[16]!='A':
					continue
				if keeptype=='sc':
					f.write(line)
				else:
					if line[12:16].strip() in keepdicts[keeptype]:
						f.write(line)
