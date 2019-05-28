class ExqUtils(object):
    def __init__(self):
        pass

    @staticmethod
    def load_file_as_iter(path):
        with open(path, "r+") as f:
            for i in f:
                yield i
