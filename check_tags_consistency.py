#!/usr/bin/env python
#
# Check that no keyword belongs to two files of tags/*
import os
d={}
good=True
for t in os.listdir("tags/"):
    with open('tags/'+t,'r') as f:
        txt=[x.strip() for x in f.readlines()]
    for x in txt:
        if d.get(x,t) != t:
            print "{}: {}|{}".format(x,t,d[x])
            good=False
        d[x]=t
if good:
    print "It's all good !"
