try:
    data
except NameError:
    from load_parsed import load_parsed
    data=load_parsed(shattered=False)
    import re
    initials=re.compile('[A-Z]\.[ ,]*')
    punc=re.compile('[,:;\. ]+')
    print "Add some fingerprints"
    for x in data:
        if 'authors' in x:
            x['fullnames'] = re.sub(punc,', ',re.sub(initials,'',x['authors'].replace(' and ',' ')))
        if 'journal' in x:
            x['journal_init'] = re.sub('[^A-Z]','',x['journal'])

class DisjointSets:
    def __init__(self):
        self._data = {}

    def get_repr(self,i):
        if i not in self._data:
            self._data[i] = i
        if self._data[i] != i:
            self._data[i] = self.get_repr(self._data[i])
        return self._data[i]

    def union(self,i,j):
        self._data[self.get_repr(i)]=self.get_repr(j)

    def len(self):
        s=set()
        for i in range(len(self._data)):
            s.add(self.get_repr(i))
        return len(s)

    def groups(self):
        groups = {}
        for p in self._data:
            key = self.get_repr(p)
            if key not in groups:
                groups[key] = []
            groups[key].append(p)
        return groups.values()

def group(*kwds):
    print 'grouping by',kwds
    d = {}
    for i,p in enumerate(data):
        try:
            key = tuple(p[x].lower() for x in kwds)
        except KeyError:
            continue
        s.union(i,d.get(key,i))
        d[key] = i
    if not d:
        raise Exception("Those keywords never appear together: {}".format(kwds))

try:
    s
except NameError:
    s = DisjointSets()
    group('title','pages')
    group('title','issue')
    group('title','vol')
    group('title','fullnames')
    group('pages','fullnames','vol')
    group('issue','pages','journal_init') # alias of journals names :-/
    group('fullnames','pages','journal_init') # alias of journals names :-/
    group('doi')
    group('arxiv')

journals_dd = DisjointSets()
for g in s.groups():
    g = [data[x]['journal'] for x in g if 'journal' in data[x]]
    for x in g:
        journals_dd.union(g[0],x)

def explain(A):
    for g in s.groups():
        g = [data[x] for x in g]
        js = set([x['journal'] for x in g if 'journal' in x])

        if any(x in js for x in A) and any(x not in A for x in js):
            for x in g:
                print x
            print '-'*20
            gg=g
