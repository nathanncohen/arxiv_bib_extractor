# -*- coding: utf-8 -*-
import re
import codecs
def get_tag(s,x):
    st=s.index(x+'=')+len(x)+1
    return s[st:s.index('╣',st)]

def load_parsed(shattered=False):
    entries = codecs.open("../all_parsed",'r',encoding='utf8').readlines()
    if shattered:
        regex = re.compile(ur"^([ ,0-9[[:punct:]]]*╠[^╣]*╣[ ,0-9[[:punct:]]]*)*$")
        entries = [x for x in entries if re.match(regex,x)]

    return [dict(re.findall(ur"╠([^=╣]*)=*([^╣]*)╣",x))
            for x in entries]
