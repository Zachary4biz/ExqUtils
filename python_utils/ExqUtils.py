class ExqUtils(object):
    def __init__(self):
        pass

    @staticmethod
    def loadFileAsIter(path):
        with open(path,"r+") as f:
            for i in f:
                yield i
