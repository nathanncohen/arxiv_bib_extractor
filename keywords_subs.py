#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import fileinput
import os
import re

d={}
for t in os.listdir("tags/"):
    with open('tags/'+t,'r') as f:
        txt=[x.strip() for x in f.readlines()]
    for x in txt:
        if d.get(x,t) != t:
            raise Exception("{}: {}|{}".format(x,t,d[x]))
        d[x]=t


kw=re.compile(r"╠\?=([^╣]*)╣")
try:
    for l in fileinput.input():
        kw=l.strip().split(u'\f')
        kwok=set()
        l=kw.pop(0)
        start = len(l)+1

        for i in range(len(kw)-1,-1,-1):
            next_start = start
            start = l.rfind(kw[i],0,start-1)
            end = start+len(kw[i])
            previous_end = 0 if i == 0 else l.rfind(kw[i-1],0,start-1)+len(kw[i-1])

            # Left and right intervals
            iright = l[end:next_start]
            ileft = l[previous_end:start]
            # print((kw[i], iright))
            # print((kw[i], ileft))

            right = bool(re.match(r"^ *[,\(\),\.0-9]",iright) or
                         re.match(r"^[\. ]*$",iright))

            left = bool(re.match(r".*[,\(;\):0-9] *$",ileft) or
                        re.match(r"^[\. ]*$",ileft) or
                        re.match(r".* [^A-Z][^ ]*\. *$",ileft))

            if left and right:
                kwok.add(i)

        start = len(l)+1
        for i in range(len(kw)-1,-1,-1):
            start = l.rfind(kw[i],0,start-1)
            if i not in kwok:
                continue
            l = l[:start]+", ╠"+d[kw[i]]+"="+kw[i]+"╣, "+l[start+len(kw[i]):]


        # "s/([,\(;\):0-9] *)$content_reg *([\(\),\.0-9])"

        #print ()
        print(l),
        # failed = [w for i,w in enumerate(kw) if i not in kwok]
        # if failed:
        #     print("Missed",failed)

except IOError:
    pass

# use strict;
# use utf8;

# use open qw(:std :utf8);

# binmode(STDOUT, ":utf8");

# opendir(DIR, 'tags/') or die $!;
# my %keywords;
# while (my $file = readdir(DIR)) {
#     # Use a regular expression to ignore files beginning with a period
#     next if ($file =~ m/^\./);
#     open(my $fh, '<:encoding(UTF-8)', 'tags/'.$file) or die "Could not open file '$file' $!";
#     while (my $row = <$fh>) {
# 	chomp $row;
# 	$keywords{$row}=$file;
#     }
# }
# closedir(DIR);
# #print "$keywords{$_}: $_\n" for (keys %keywords);

# foreach my $line ( <STDIN> ) {
#     chomp( $line );
#     my @arr = split(/\|/, $line);
#     print "$arr[0]\n";
#     print "$arr[1]\n";
# }
# #print "$keywords{Whatever}\n";
