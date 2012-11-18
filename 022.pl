#!/usr/bin/perl

use strict;
use warnings;
use List::Util qw(first);

my @alpha = qw(a b c d e f g h i j k l m n o p q r s t u v w x y z);
my $file = "022.txt";

my $result = 0;

open my $info, $file or die "Can't open $file: $!";

sub get_value {
	my $tmp_val = 0;

	foreach my $c ( split(undef, lc( $_[0] )) ){

		if ( $c ne "\"" && $c ne "\n" && $c ne " " ){
			my $index = first { $alpha[$_] eq $c } 0 .. $#alpha;
			if ( length $index ){
				$tmp_val += ($index+1);
			} else {
				print "Bad char: [".$c."] in ".$_[0]."\n";
			}
		}

	}
	return $tmp_val;
}


while ( my $names = <$info> ) {
	my $loc_index = 1;
	foreach my $name ( sort(split("," , $names)) ) {
		$result += (get_value( $name ) * $loc_index);
		$loc_index += 1;
	}
}

print $result;
