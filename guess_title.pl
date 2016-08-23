#!/usr/bin/perl

foreach $line ( <STDIN> ) {
    chomp( $line );
    $saved_line = $line;

    $line =~ s/^.*authors=[^╣]*╣[,\. ]*//;
    $line =~ s/╠[^y].*//g;
    $line =~ s/[, ]*╠.*?╣[, ]*/\n/g;
    print $line."\n";
    while ($x =~ /([“ ]*[[:digit:]|[:upper:]][^,\.”]*([,\. ]+[[:lower:]][^,\.]*)*)/) {
        print "Word is $x, ends at position ", pos $x, "\n";
    }
    #perl -ape "s/^( |[[:punct]]|“)*//g" | grep -P "\w{3}" | longest_line)"
    #echo "$*" | replace "$b" ", ╠title=$b╣, "

}
