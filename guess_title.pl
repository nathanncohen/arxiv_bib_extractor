#!/usr/bin/perl
use utf8;
use open ':std' => ':encoding(UTF-8)';

foreach $line ( <STDIN> ) {
    chomp( $line );
    $saved_line = $line;

    $line =~ s/^.{1,10}\]//;
    $line =~ s/^.*authors=[^╣]*╣[,\. ]*//;
    $line =~ s/╠[^y].*//g;
    $line =~ s/[, ]*╠.*?╣[, ]*/,\n/g;
    #print "--> $line\n";
    while ($line =~ /[“ [:punct:]]*([[:digit:]|[:upper:]][^,\.]*([,\. ]+[[:lower:]][^,\.]*)*)/g) {
        $title="$1";
	$title =~ s/ *https*\:.*//g;
	if ( length($title) >= 3 ) {
	    $saved_line =~ s/\Q$title\E/, ╠title=$title╣, /;
	    last;
	}
    }
    print "$saved_line\n";
}
