# -*- coding: utf-8 -*-
import re
def get_tag(s,x):
    st=s.index(x+'=')+len(x)+1
    return s[st:s.index('╣',st)]

def load_parsed():
    return [dict(re.findall("╠([^=╣]*)=*([^╣]*)",x))
            for x in open("../all_parsed",'r').readlines()]
