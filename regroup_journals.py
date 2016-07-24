# -*- coding: utf-8 -*-
from itertools import permutations, combinations
from collections import Counter
def get_tag(s,x):
    st=s.index(x+'=')+len(x)+1
    return s[st:s.index('╣',st)]

f=open('../all_parsed','r').readlines()
f=[x for x in f if 'journal=' in x and 'title=' in x]
f=[(get_tag(x,"title"),get_tag(x,"journal")) for x in f]
ff={}
for t,j in f:
    if t not in ff:
        ff[t] = []
    ff[t].append(j)
p={}
for t,jl in ff.iteritems():
    for (j1,k1),(j2,k2) in combinations(Counter(jl).iteritems(),2):
        p[j1,j2] = p.get((j1,j2),0) + k1*k2
        p[j2,j1] = p.get((j2,j1),0) + k1*k2
for k,(j1,j2) in sorted([(y,x) for x,y in p.iteritems()]):
    print "{}|{}|{}".format(k,j1,j2)
