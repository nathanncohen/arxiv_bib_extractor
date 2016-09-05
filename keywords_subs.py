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

journals_set = {x for x,v in d.items() if v=='journal'}

cardinal_regex="(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth|twenty|thirty|forty|fifty|[0-9]+ *[a-z]{2}| |-)+"
proceedings_regex=re.compile("([^A-Z][^ ]*\.|,)(?P<prefix> *(in|:|the|proc(\.|eedings)|of|"+cardinal_regex+"|Annual|International|Conf(erence|\.)*|workshop|on| )*)$", re.IGNORECASE)


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

            right = (re.match(r" *[,\.0-9\(\)]",iright) or
                     (re.match(r"[\.,;: ]*$",iright) and i+1 in kwok))

            left = right and bool(re.search(r"[,\(;\):0-9\?] *$",ileft) or
                                  re.search(r"^[\.,;: ]*$",ileft) or
                                  re.search(r" [^A-Z][^ ]*\. *$",ileft) or
                                  (kw[i] in journals_set and re.search(r"\. *$",ileft)))

            if right and not left and kw[i] in journals_set:
                m = re.search(proceedings_regex, l[:start].strip())
                if m:
                    left = True
                    start -= len(m.group('prefix'))

            if left and right:
                kwok.add(i)
                l = l[:start]+", ╠"+d[kw[i]]+"="+kw[i]+"╣, "+l[end:]

        print(l),

except IOError:
    pass
