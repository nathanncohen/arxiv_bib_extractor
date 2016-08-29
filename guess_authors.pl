#!/usr/bin/perl

# function guess_authors () {
#     b="$(echo "$*" | sed "s/^.*\] *//"g | sed "s/[”“╠[:digit:]].*//g")"

#     # Starts with Initials.
#     # Meant to match the following pattern: I. K. Whatever, K.L. Whateverrr[.,] and O. Thing and J. van der Stuff[.,]
#     if [ "${b:1:1}" = "." ]; then
# 	aut="$(echo $b | \grep -P -o "^(((([[:upper:]]\.[- ]*)+,*)+ *([a-z]{1,4} )*)[^ ]+( and|[[:punct:]]) *)*")"
# 	echo "$*" | replace "$aut" "╠authors=$aut╣, "
# 	return 0
#     fi

#     # Same in the other order, i.e. Whatever I. K., Whateverrrrr K. L., #
#     aut="$(echo $b | \grep -P -o "^((\w{1,4} )*[^ ]+[[:punct:]]* +([[:upper:]][[:punct:]]+ *)+( and|[[:punct:]])* *)*(et al\.[ [[:punct:]]]*)*")"
#     if [ -n "$aut" ]; then
# 	echo "$*" | replace "$aut" "╠authors=$aut╣, "
# 	return 0
#     fi

#     # Victor P. Whatever, Nicolas E. G. H. H. Thingy, and Whatever Whathehell,
#     aut="$(echo "$b" | grep -P -o "^([[:upper:]][^ ,\.:;]+ ([[:upper:]]\. +)*[[:upper:]][^ ,\.:;]+([,\.:;]* and|[,\.:;]) +)+")"
#     if [ -n "$aut" ]; then
# 	echo "$*" | replace "$aut" "╠authors=$aut╣, "
# 	return 0
#     fi

#     echo "$*"
# }

$surname='(\b\w{1,4}\b )*[[:upper:]][^ ]+\b';
$initials='(( *\b[[:upper:]]\.[ -,]*)+)';
$fullname='[[:upper:]][^ ]+\b +('.$initials.')* *\b'.$surname; # Monkey D. Luffy or Ludwig van Beethoven
$name_and_initial=$surname."[[:punct:]]* +$initials"; # Whatever I. K., Whateverrrrr K. L.

foreach $line ( <STDIN> ) {
    chomp( $line );
    $saved_line = $line;

    $line =~ s/^.*\] *//g;
    $line =~ s/[”“╠[:digit:]].*//g;
    #print $line."<<-\n";

    # Starts with Initials.
    # Meant to match the following pattern: I. K. Whatever, K.L. Whateverrr[.,] and O. Thing and J. van der Stuff[.,]
    if ( $line =~ /^.\./ &&
	 $line =~ /^(((($initials,*)+ *)+ *$surname(,* and,*|[[:punct:]]) *)+)/
	) {
	$aut=$1;
    }

    # Same in the other order, i.e. Whatever I. K., Whateverrrrr K. L., #
    #    elsif ( $line =~ /(^((\w{1,4} )*[^ ]+[[:punct:]]* +([[:upper:]][[:punct:]]+ *)+( and|[[:punct:]])* *)*(et al\.[ [[:punct:]]]*)+)/ ) {
    elsif ( $line =~ /(^($name_and_initial([[:punct:]]+|and)+ *)+)/ ) {
	$aut = $1;
    }

    # Victor P. Whatever, Nicolas E. G. H. H. Thingy, and Whatever Whathehell,
    elsif ( $line =~ /(^([[:upper:]][^ ,\.:;]+ ([[:upper:]]\. +)*$surname([,\.:;]* and|[,\.:;]) +)+)/ ) {
	$aut = $1;
    }

    # Corrado De Concini and Claudio Procesi (many names, with an 'and')
    elsif ( $line =~ /^((($fullname(, | and ))*)*$fullname and $fullname)/) {
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
