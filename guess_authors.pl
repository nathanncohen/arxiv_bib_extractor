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
foreach $line ( <STDIN> ) {
    chomp( $line );
    $saved_line = $line;

    $line =~ s/^.*\] *//g;
    $line =~ s/[”“╠[:digit:]].*//g;
    if ( $line =~ /^.\./ &&
	 $line =~ /^((((([[:upper:]]\.[- ]*)+,*)+ *([a-z]{1,4} )*)[^ ]+( and|[[:punct:]]) *)*)/
	) {
	$aut=$1;
    }
    elsif ( $line =~ /(^((\w{1,4} )*[^ ]+[[:punct:]]* +([[:upper:]][[:punct:]]+ *)+( and|[[:punct:]])* *)*(et al\.[ [[:punct:]]]*)*)/ ) {
	$aut = $1;
    }
    elsif ( $line =~ /(^([[:upper:]][^ ,\.:;]+ ([[:upper:]]\. +)*[[:upper:]][^ ,\.:;]+([,\.:;]* and|[,\.:;]) +)+)/ ) {
	$aut = $1;
    }

    if ( $aut ) {
	$saved_line =~ s/\Q$aut\E/╠authors=$aut╣, /;
    }
    print(($saved_line)."\n");

}
