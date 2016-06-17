with open("index",'r') as f:
    d = [x.strip() for x in f.readlines()]

from collections import Counter
for x,_ in sorted(Counter(d).items(),key=lambda x:x[1])[-20:-1]:
    x=Word(x)
    l = .8*len(x)
    print [y for y in set(d) if len(y)<=2*l and len(x.longest_common_subword(y))>=l]
