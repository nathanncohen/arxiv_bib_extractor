#!/usr/bin/perl

# use feature 'unicode_strings';
# use open qw(:std :utf8);
# binmode STDOUT, ':utf8';
#use open ':encoding(utf8)';
#binmode(STDOUT, ":utf8");
use utf8;
use open ':std' => ':encoding(UTF-8)';


$surname='(\w{1,3} +)*?\p{Upper}[^ ,\.]+';
$initials='(([ -]*\p{Upper}\p{Lower}?\.[ -,]*)+)';
$fullname='\p{Upper}[^ ]+ +('.$initials.')* *\b'.$surname; # Monkey D. Luffy or Ludwig van Beethoven
$name_and_initial=$surname."[[:punct:]]* +$initials"; # Whatever I. K., Whateverrrrr K. L.

foreach $line ( <STDIN> ) {
    chomp( $line );
    $saved_line = $line;

    $line =~ s/^.*\] *//g;
    $line =~ s/(”|“|╠|[[:digit:]]).*//g;
    #print $line."<<-\n";

    # Starts with Initials.
    # Meant to match the following pattern: I. K. Whatever, K.L. Whateverrr[.,] and O. Thing and J. van der Stuff[.,]
    if ( $line =~ /^.\./ &&
	 $line =~ /^((($initials,*)+ +$surname( (&|and)|[[:punct:]])+ *)*(($initials,*)+ +$surname[ [:punct:]]*))/
	) {
	$aut=$1;
    }

    # Same in the other order, i.e. Whatever I. K., Whateverrrrr K. L., #
    #    elsif ( $line =~ /(^((\w{1,4} )*[^ ]+[[:punct:]]* +([[:upper:]][[:punct:]]+ *)+( and|[[:punct:]])* *)*(et al\.[ [[:punct:]]]*)+)/ ) {
    elsif ( $line =~ /(^($name_and_initial([[:punct:]]+|and|\&)+ *)+)/ ) {
	$aut = $1;
    }

    # Victor P. Whatever, Nicolas E. G. H. H. Thingy, and Whatever Whathehell,
    elsif ( $line =~ /(^([[:upper:]][^ ,\.:;]+ ([[:upper:]]\. +)*$surname([,\.:;]* (&|and)|[,\.:;]) +)+)/ ) {
	$aut = $1;
    }

    # Corrado De Concini and Claudio Procesi (many names, with an 'and')
    elsif ( $line =~ /^((($fullname(, | (&|and) ))*)*$fullname and $fullname)/) {
	$aut = $1;
    }
    elsif ( $line =~ /^($fullname[\., ]*)/) {
	$aut = $1;
    }

    if ( $aut ) {
	#print("triggered\n");
	$saved_line =~ s/\Q$aut\E/╠authors=$aut╣, /;
    }
    print(($saved_line)."\n");

}
