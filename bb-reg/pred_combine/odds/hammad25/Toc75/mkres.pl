$a = shift @ARGV;
open(STRUCT, "<$a.fasta") || die "Couldn't open file\n";
open(RES, ">$a.res") || die "Couldn't open file\n";
$i = 1;
while(<STRUCT>) 
{
	@arr = split(' ',$_);
	$len = length($arr[0]);
	for($i=0; $i<$len; $i++)
	{
		$aa = substr($arr[0],$i,1);
		printf RES "%d\n",aatoid($aa);
	}
}
sub aatoid {
    my $aa = $_[0];
    if($aa eq "A") { return  0; }
    if($aa eq "R") { return  1; }
    if($aa eq "N") { return  2; }
    if($aa eq "D") { return  3; }
    if($aa eq "C") { return  4; }
    if($aa eq "Q") { return  5; }
    if($aa eq "E") { return  6; }
    if($aa eq "G") { return  7; }
    if($aa eq "H") { return  8; }
    if($aa eq "I") { return  9; }
    if($aa eq "L") { return 10; }
    if($aa eq "K") { return 11; }
    if($aa eq "M") { return 12; }
    if($aa eq "F") { return 13; }
    if($aa eq "P") { return 14; }
    if($aa eq "S") { return 15; }
    if($aa eq "T") { return 16; }
    if($aa eq "W") { return 17; }
    if($aa eq "Y") { return 18; }
    if($aa eq "V") { return 19; }
}
#awk '{print $2, $5, $4}' 1A0S.dssp >1A0S.struct
#awk '{print $2, $5, $3}' 1BXW.dssp >1BXW.struct
