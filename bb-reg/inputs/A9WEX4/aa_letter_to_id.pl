#!/usr/bin/perl
use strict;
use warnings;

if (scalar(@ARGV) != 2) {
	die "I need 2 args: the sequence file and the output name\n";
}
my $in = $ARGV[0];
my $out = $ARGV[1];

open IN, "<$in" or die $!;
my $line = <IN>;
chomp($line);
close IN;
my $c = "";
open OUT, ">$out" or die $!;
for (my $i = 0; $i<length($line); $i++) {
	$c = substr($line, $i, 1);
	$c = uc($c);
	print OUT aatoid($c) . "\n";
}
close OUT;

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