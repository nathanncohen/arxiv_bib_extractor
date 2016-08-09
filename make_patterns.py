# -*- coding: utf-8 -*-
import re
from collections import Counter
from string import join
import os

possible_categories=set(os.listdir('tags'))


def get_pattern(s):
    return [xx.replace('╠','') for xx in re.findall("╠[^╣=]*",s)]

shattered=re.compile("^([\(\):; 0-9,\.]*╠[^╣]*╣[\(\):; 0-9,\.]*)*$")

def get_patterns(f):
    #f=[x for x in f if re.match(shattered,x)]
    f=map(get_pattern,f)
    return Counter(map(tuple,f))

try:
    all_parsed
except:
    all_parsed=open("/home/ncohen/all_parsed",'r').readlines()
    all_parsed=[x.strip() for x in all_parsed]
    f=get_patterns(all_parsed)

for p,c in sorted(f.iteritems(), key=lambda x:x[1]):
    print join(p,',')+',',c

try:
    d
except:
    d={}
    for p,c in f.iteritems():
        for i in range(len(p)):
            if p[i] not in possible_categories:
                continue
            pp=list(p)
            pp[i] = 'unknown'
            pp=tuple(pp)
            if pp not in d:
                d[pp]={}
            d[pp][p[i]] = c

def classify(s):
    print s
    isin=re.compile(".*[,\.:; ]+"+s+"[,\.:; ]+.*")
    print isin
    for x in all_parsed:
        if s in x:
            print x
    f = [x for x in all_parsed if re.match(isin,x)]
    f = [re.sub(s,', ╠unknown╣, ',x) for x in f]
    f = get_patterns(f)
    freq = {}
    for x,c in f.items():
        tot = sum(d.get(x,{}).values())+0.
        print d.get(x,{})
        for k,cc in d.get(x,{}).iteritems():
            freq[k] = freq.get(k,0) + c*cc/tot
    return freq
