targetStr=[
    "alpha","alloha","allright",
    "basic","batch",
    "mark","marval"
]

class TrieTree(object):
    def __init__(self,targets=None):
        if targets is None:
            targets = []
        self.targets=targets
        self.tree = {}
        self.build()
        self.END="-1"
    
    def build(self):
        for word in self.targets:
            self.add(word)
            
    def add(self,word):
        tree = self.tree
        for char in word:
            if char in tree:
                tree = tree[char]
            else:
                tree[char]={}
                tree = tree[char]

    def exists(self,word):
        tree = self.tree
        for idx,char in enumerate(word):
            if char in tree:
                tree = tree[char]
            else:
                if idx==len(word)-1:
                    return True
                else:
                    return False
        return True
    
t=TrieTree()
for i in targetStr:
    t.add(i)

for i in targetStr:
    print(i,t.exists(i))