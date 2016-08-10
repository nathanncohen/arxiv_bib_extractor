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
        l=l.strip()
        for x in re.findall(kw,l):
            l=l.replace("╠?={}╣".format(x),"╠{}={}╣".format(d[x],x))
        print(l)
except IOError:
    pass
