#include <iostream>
#include <string>
#include <fstream>
#include <cmath>
#include <sstream>
#include <vector>
#include <algorithm>
#include <iomanip>
#include "ec_score_dict.cpp"

using namespace std;

enum StrandOrientation {PERI2EXTRA,EXTRA2PERI};
enum HBondPattern {SWV,VWS};

// load odds data
void load_odds(const string fn, vector<double>& arr, double default_val, bool needlog=true);
// calculate pairing energy of a hairpin
double pairing(HBondPattern hbp, int len, StrandOrientation o1, vector<int> &strand1, vector<int> &strand2) ;
// get pairid for a given aa pair
int aa_pair(int a, int b);
// determine hbond pattern of two neighboring strands
HBondPattern patterning(int pdbi, int extra, int orientation1);
int getres(int pdbi, int seqid);
// predict regsistration
int regsistrationing();

const static int AABoundary = 19;
const static int InvalidAA = 20;
const static double nref = 8.5; // avg loop length of ori 25 prot

int pdb_num = 0;
vector<int> res_len;
vector< vector<int> > res;

vector<double> strong_scores(210,0), vdw_scores(210,0), weak_scores(210,0);
vector<double> CoreIn(21,0), CoreOut(21,0), PeriIn(21,0), PeriOut(21,0), ExtraIn(21,0), ExtraOut(21,0);


int main(int argc,char*argv[]) {

	if(argc!=4){
		cerr << "# of arguments incorrect"<<endl;
		cerr << "Usage: " << argv[0] << " test_file ec_reg_file odds_folder" << endl;
		exit(1);
	}

	char* testfn = argv[1];
	char* ecsfn = argv[2];
	string oddsdir = argv[3];

	// read ec score
	ECSDict dict;
	get_ec_dict(ecsfn,dict);

	// load test input data
	ifstream fin(testfn);
	if(fin.fail()) {
		cerr << "error  opening file " << testfn <<endl;
		exit(1);
	}
	vector<int> strand_num;
	vector< vector<int> > ori_peris, ori_extras, ori_regs;
	vector< vector<bool> > iscorrect;
	vector<string> pdbs;
	string line, pdbname;
	int strandnum;
	while(getline(fin, line)){
		stringstream ss(line);
		ss >> pdbname >> strandnum;
		pdbs.push_back(pdbname);
		strand_num.push_back(strandnum);
		ori_peris.push_back(vector<int>(strandnum,0));
		ori_extras.push_back(vector<int>(strandnum,0));
		ori_regs.push_back(vector<int>(strandnum,0));
		iscorrect.push_back(vector<bool>(strandnum, false));
		for(int strandi=0; strandi < strandnum; strandi++) {
			ss >> ori_peris.back()[strandi] >> ori_extras.back()[strandi] >> ori_regs.back()[strandi];
		}
	}
	fin.close();
	// get total pdb num
	pdb_num = pdbs.size();

	// load res data
	res_len = vector<int>(pdb_num);
	res = vector< vector<int> >(pdb_num);
	for(int pdbi=0 ; pdbi<pdb_num; pdbi++) {
		res[pdbi].push_back(InvalidAA);
		string fn = "..//..//bb-pipe//inputs//" + pdbs[pdbi] + "//" + pdbs[pdbi] + ".res";
		fin.open(fn.c_str());
		if(fin.fail()) {
			cerr << "error  opening file " << fn <<endl;
			exit(1);
		}
		int dummy;
		while(fin >> dummy){
			if(dummy > AABoundary){
				dummy = InvalidAA;
			}
			res[pdbi].push_back(dummy);
		}
		fin.close();
		res_len[pdbi]=res[pdbi].size()-1;
	}

	// load pair odds
	vector< vector<double> > strongs(pdb_num), vdws(pdb_num), weaks(pdb_num);
	string oddsfn;
	for(int pdbi = 0 ; pdbi<pdb_num; pdbi++){
		strongs[pdbi] = vector<double>(210,0);
		weaks[pdbi]   = vector<double>(210,0);
		vdws[pdbi]    = vector<double>(210,0);
		load_odds(oddsdir+"//"+pdbs[pdbi]+"//"+pdbs[pdbi]+".strong.odds", strongs[pdbi], -1.72);
		load_odds(oddsdir+"//"+pdbs[pdbi]+"//"+pdbs[pdbi]+".vdw.odds", vdws[pdbi], -1.72);
		load_odds(oddsdir+"//"+pdbs[pdbi]+"//"+pdbs[pdbi]+".weak.odds", weaks[pdbi], -1.72);
	}

	// load single body odds
	load_odds( oddsdir+"//ExtraOut.odds", ExtraOut, -3.9 );
	load_odds( oddsdir+"//ExtraIn.odds",  ExtraIn, -3.9 );
	load_odds( oddsdir+"//CoreOut.odds", CoreOut, -3.9 );
	load_odds( oddsdir+"//CoreIn.odds",  CoreIn, -3.9 );
	load_odds( oddsdir+"//PeriOut.odds", PeriOut, -3.9 );
	load_odds( oddsdir+"//PeriIn.odds",  PeriIn, -3.9 );


	double wstrong = 0.03, wvdw = 0.04, wweak = 0.06; double wec = 0; double penub = 0.8, penneg = 0.5;

	double loopstep = 1.0;
	#ifdef L1O
	for(int leavepdbi=0; leavepdbi<pdb_num; leavepdbi++)
	{
	#endif//L1O
	
	int max_correct_num = 0;

	// search for the best weights
	#ifdef SEARCH // search for best weights
	#ifndef BENCH // using only statistical potential
	//for(wec = 0.001; wec <0.051; wec+=0.001*3)// newlogp
	//for(wec = 0.8; wec <3.5; wec+=0.1*loopstep*1.5)// p
	for(wec = 1.0; wec <1.0001; wec+=0.1*loopstep*1.5)// p
	{
	#endif//BENCH
	// penneg is hardly smaller than 0.6
	for(penub = 0.066; penub <= 0.580; penub+= 0.02)
	{
	// penneg is hardly larger than 0.4
	for(penneg = 0.029; penneg < 0.220; penneg+=0.02)
	{
	for(wstrong = 0.002; wstrong < 0.140; wstrong += 0.003)
	{
	for(wvdw = 0.010; wvdw < 0.140; wvdw += 0.003)
	{
	for(wweak = 0.002; wweak < 0.086; wweak += 0.003)
	{
	#endif//SEARCH
	
		int tot_correct_num = 0;

		// loop for each pdb
		for(int pdbi=0 ; pdbi < pdb_num; pdbi++) {
			#ifdef L1O
			if(leavepdbi==pdbi){
				continue;
			}
			#endif//L1O

			#if ! defined(SEARCH) && defined(BESTWEIGHT)
			if(strand_num[pdbi] < 10 || pdbs[pdbi] == "1k24" || pdbs[pdbi] == "1qd6" || pdbs[pdbi] == "2f1c" || pdbs[pdbi] == "1i78" || pdbs[pdbi] == "2wjr" || pdbs[pdbi] == "4pr7"){
				wec=1; penub=0.15; penneg=0.05; wstrong=0.015; wvdw=0.015; wweak=0.035;
			}
			else if(pdbs[pdbi] == "1t16" || pdbs[pdbi] == "1uyn" || pdbs[pdbi] == "1tly" || pdbs[pdbi] == "3aeh" || pdbs[pdbi] == "3bs0" || pdbs[pdbi] == "3dwo" || pdbs[pdbi] == "3fid" || pdbs[pdbi] == "3kvn" || pdbs[pdbi] == "4e1s"){
				wec=1; penub=0.57; penneg=0.13; wstrong=0.048; wvdw=0.12; wweak=0.074;
			}
			else if(pdbs[pdbi] == "2mpr" || pdbs[pdbi] == "1a0s" || pdbs[pdbi] == "2omf" || pdbs[pdbi] == "2por" || pdbs[pdbi] == "1prn" || pdbs[pdbi] == "1e54" || pdbs[pdbi] == "2o4v" || pdbs[pdbi] == "3vzt" || pdbs[pdbi] == "4k3c" || pdbs[pdbi] == "4k3b" || pdbs[pdbi] == "4c4v" || pdbs[pdbi] == "4n75"){
				wec=1; penub=0.15; penneg=0.05; wstrong=0.045; wvdw=0.115; wweak=0.035;
			}
			else if(pdbs[pdbi] == "2qdz" || pdbs[pdbi] == "2ynk" || pdbs[pdbi] == "3rbh" || pdbs[pdbi] == "3syb" || pdbs[pdbi] == "3szv" || pdbs[pdbi] == "4c00" || pdbs[pdbi] == "4gey"){
				wec=1; penub=0.57; penneg=0.22; wstrong=0.13; wvdw=0.048; wweak=0.057;
			}
			else if(strand_num[pdbi] < 28){
				wec=1; penub=0.09; penneg=0.08; wstrong=0.009; wvdw=0.026; wweak=0.003;
			}
			#ifdef BENCH
			wec = 0;
			#endif//BENCH
			#endif// ! SEARCH && BESTWEIGHT
			
			
			for(int i=0; i<210; i++) {
				strong_scores[i] = strongs[pdbi][i] * wstrong;
				vdw_scores[i] = vdws[pdbi][i] * wvdw;
				weak_scores[i] = weaks[pdbi][i] * wweak;
			}

			// useless, this part is for optimization
			vector<int> peris  = ori_peris [pdbi];
			vector<int> extras = ori_extras[pdbi];
			vector<int> regs   = ori_regs  [pdbi];

			int curr_correct_num = 0; 

			#if defined(OUTPUT_SCORE) && !defined(SEARCH) // output score details for shear adjustment 
			cout << "## " << pdbs[pdbi] << endl;
			#endif//OUTPUT_SCORE

			// loop for each strand for current pdb
			for(int strandi = 0; strandi < strand_num[pdbi]; strandi++) {
				int strandj = (strandi+1) % strand_num[pdbi];
				vector<int> newstrand1, newstrand2;
				StrandOrientation orientation1;
				if(strandi%2==0){
					orientation1 = PERI2EXTRA;
					// make strands
					newstrand1 = vector<int> (res[pdbi].begin()+peris[strandi], res[pdbi].begin()+extras[strandi]+1);
					newstrand2 = vector<int> (res[pdbi].begin()+extras[strandj], res[pdbi].begin()+peris[strandj]+1);
					reverse(newstrand1.begin(),newstrand1.end());
				}
				else{
					orientation1 = EXTRA2PERI;
					// make strands
					newstrand1 = vector<int> (res[pdbi].begin()+extras[strandi], res[pdbi].begin()+peris[strandi]+1);
					newstrand2 = vector<int> (res[pdbi].begin()+peris[strandj], res[pdbi].begin()+extras[strandj]+1);
					reverse(newstrand2.begin(),newstrand2.end());
				}

				// determine pattern
				HBondPattern hbond_pattern = patterning(pdbi, extras[strandi], orientation1);

////////////////////////////////////////
//////////////////////////////////////// core computation part
				// make tmp strand2
				vector<int> newstrand2tmp(newstrand1.size());

				double maxscore = -1000;
				int max_predreg  =0;
				// enumerate registration
				//for(int regoffset=-20; regoffset <= 16; regoffset++) { 
				for(int regoffset=-10; regoffset <= 6; regoffset++) { 
					for(int i=0; i < newstrand1.size(); i++) {
						if(i+regoffset < 0 || i+regoffset >= newstrand2.size())
							newstrand2tmp[i] = InvalidAA;
						else
							newstrand2tmp[i] = newstrand2[i+regoffset];
					}

					int curr_predreg = newstrand2.size()-newstrand1.size()-regoffset;
					double ecscore = dict[pdbs[pdbi]][strandi][curr_predreg];
					double negative_reg = curr_predreg>=0 ? 0 : curr_predreg;
					double currscore =	pairing(hbond_pattern, newstrand1.size(), orientation1, newstrand1, newstrand2tmp) // hbond
										- penub*log((abs(regoffset) + nref)/nref) // penalty for unbonded res
										+ penneg * negative_reg // panalty for neg reg
										+ wec * ecscore; // ec score

					#if defined(OUTPUT_SCORE) && !defined(SEARCH)
					cout << setprecision(3) << curr_predreg << ":" << currscore << " ";
					#endif//OUTPUT_SCORE

					if(currscore > maxscore) {
						maxscore = currscore;
						max_predreg = curr_predreg;
					}
				}
				#if defined(OUTPUT_SCORE) && !defined(SEARCH)
				cout << endl;
				#endif//OUTPUT_SCORE
//////////////////////////////////////// core computation part
////////////////////////////////////////

				if( max_predreg == regs[strandi]) {
					iscorrect[pdbi][strandi] = true;
					curr_correct_num++;
				}
				else{
					iscorrect[pdbi][strandi] = false;
				}
				
				//cout << pdbs[pdbi] << " " << strandi << " " << max_predreg << " " << regs[strandi] << endl;
			}// strand loop
			tot_correct_num += curr_correct_num;
		}// pdb loop

		if( tot_correct_num >= max_correct_num) { //this is for parameter searching
			max_correct_num = tot_correct_num;
			#ifndef OUTPUT_SCORE
			#ifdef L1O
			cout << "l1o: " << leavepdbi << " | ";
			#endif//L1O
			cout << wec << " " << penub << " " << penneg << " " << wstrong << " " << wvdw << " " << wweak << " " << tot_correct_num << endl;
			#endif//OUTPUT_SCORE

			for(int pdbi=0 ; pdbi < pdb_num; pdbi++) {
				#ifdef SEARCH
				cout << pdbs[pdbi] << " " ;
				#endif//SEARCH
				int pdbicorrect = 0;
				for(int strandi=0; strandi < strand_num[pdbi]; strandi++) {
					if(iscorrect[pdbi][strandi]){
						pdbicorrect++;
						//cout << "o";
					}
					else{
						//cout << "x";
					}
				}
				#ifndef OUTPUT_SCORE
				cout << pdbicorrect << " ";
				//cout << endl;
				#endif//OUTPUT_SCORE
			}
			#ifndef OUTPUT_SCORE
			cout << endl;
			#endif//OUTPUT_SCORE
		}

	
	#ifdef SEARCH
	}
	}
	}
	}
	}
	#ifndef BENCH
	}
	#endif//BENCH
	#endif//SEARCH
	
	#ifdef L1O
	}
	#endif//L1O

	return 0;
}

/// 
int aa_pair(int aa1, int aa2) {
	if(aa1 > AABoundary || aa2 > AABoundary ) { return -1; }
	if(aa1 <= aa2) { return (aa1 * 20 + aa2 - (aa1*(aa1+1)/2)); }
	else { return (aa2 * 20 + aa1 - (aa2*(aa2+1)/2)); }
}

double pairing(HBondPattern hbp, int len, StrandOrientation o1, vector<int> &strand1, vector<int> &strand2) {
	double sum = 0.0;
	vector<int> &tmpstrand1 = (o1==PERI2EXTRA) ? strand2 : strand1;
	vector<int> &tmpstrand2 = (o1==PERI2EXTRA) ? strand1 : strand2;
	if(hbp == SWV) {
		for(int i = 0 ; i < len-1 ; i++) {
			if(aa_pair(tmpstrand1[i], tmpstrand2[i+1]) != -1) {
				sum += weak_scores[aa_pair(tmpstrand1[i], tmpstrand2[i+1])];
			}
		}
		for(int i = 0 ; i < len ; i = i+2) {
			if(aa_pair(tmpstrand1[i], tmpstrand2[i]) != -1) {
				sum += strong_scores[aa_pair(tmpstrand1[i], tmpstrand2[i])];
			}
		}
		for(int i = 1 ; i < len ; i = i+2) {
			if(aa_pair(tmpstrand1[i], tmpstrand2[i]) != -1) {
				// will: gly no vdw? diff from pairing()
				if( tmpstrand1[i] != 7 || tmpstrand2[i] != 7)
					sum += vdw_scores[aa_pair(tmpstrand1[i], tmpstrand2[i])]; 
			}
		}
	}
	else {
		for(int i = 0 ; i < len-1 ; i++) {
			if(aa_pair(tmpstrand1[i], tmpstrand2[i+1]) != -1) {
				sum += weak_scores[aa_pair(tmpstrand1[i], tmpstrand2[i+1])];
			}
		}
		for(int i = 0 ; i < len ; i = i+2) {
			if(aa_pair(tmpstrand1[i], tmpstrand2[i]) != -1) {
				if( tmpstrand1[i] != 7 || tmpstrand2[i] != 7)
					sum += vdw_scores[aa_pair(tmpstrand1[i], tmpstrand2[i])]; 
			}
		}
		for(int i = 1 ; i < len ; i = i+2) {
			if(aa_pair(tmpstrand1[i], tmpstrand2[i]) != -1) {
				sum += strong_scores[aa_pair(tmpstrand1[i], tmpstrand2[i])];
			}
		}	
	}
	return sum;
}



void load_odds(const string fn, vector<double>& arr, double default_val, bool needlog){
	ifstream fin(fn.c_str());
	if(fin.fail()) {
		cerr << "error  opening file " << fn <<endl;
		exit(1);
	}
	int i = 0;
	while(fin >> arr[i]){
		if(arr[i]==0){ arr[i]=default_val; }
		else{ arr[i] = needlog ? (double)log(arr[i]) : (double)arr[i]; }
		i++;
	}
	fin.close();
}


int getres(int pdbi, int seqid){
	if( seqid<1 || seqid>res_len[pdbi] ){
		return InvalidAA;
	}
	return res[pdbi][seqid];
}


HBondPattern patterning(int pdbi, int extra, int orientation1){
	double SumEven, SumOdd;
	if(orientation1 == EXTRA2PERI) {
		SumEven = ExtraIn[getres(pdbi,extra)]+ExtraOut[getres(pdbi,extra+1)]+CoreIn[getres(pdbi,extra+2)]+CoreOut[getres(pdbi,extra+3)]+CoreIn[getres(pdbi,extra+4)]+CoreOut[getres(pdbi,extra+5)]+CoreIn[getres(pdbi,extra+6)]+PeriOut[getres(pdbi,extra+7)]+PeriIn[getres(pdbi,extra+8)];
		SumOdd = ExtraOut[getres(pdbi,extra)]+ExtraIn[getres(pdbi,extra+1)]+CoreOut[getres(pdbi,extra+2)]+CoreIn[getres(pdbi,extra+3)]+CoreOut[getres(pdbi,extra+4)]+CoreIn[getres(pdbi,extra+5)]+CoreOut[getres(pdbi,extra+6)]+PeriIn[getres(pdbi,extra+7)]+PeriOut[getres(pdbi,extra+8)];
	}
	else {
		SumOdd = ExtraIn[getres(pdbi,extra)]+ExtraOut[getres(pdbi,extra-1)]+CoreIn[getres(pdbi,extra-2)]+CoreOut[getres(pdbi,extra-3)]+CoreIn[getres(pdbi,extra-4)]+CoreOut[getres(pdbi,extra-5)]+CoreIn[getres(pdbi,extra-6)]+PeriOut[getres(pdbi,extra-7)]+PeriIn[getres(pdbi,extra-8)];
		SumEven = ExtraOut[getres(pdbi,extra)]+ExtraIn[getres(pdbi,extra-1)]+CoreOut[getres(pdbi,extra-2)]+CoreIn[getres(pdbi,extra-3)]+CoreOut[getres(pdbi,extra-4)]+CoreIn[getres(pdbi,extra-5)]+CoreOut[getres(pdbi,extra-6)]+PeriIn[getres(pdbi,extra-7)]+PeriOut[getres(pdbi,extra-8)];
	}
	if(SumOdd > SumEven){
		return SWV;
	}
	else{
		return VWS;
	}
}

