class SeqItem():

    def __init__(self, DATA_W = 4, THRESHOLD = 8):
        self.THRESHOLD:  int = THRESHOLD
        self.DATA_W:  int = DATA_W
        self.valid:  int = 0
        self.data:   int = 0

    def set_values(self, data: int, valid: int = 1):
        self.data = data
        self.valid = valid

    def __iter__(self):
        objects = ['DATA_W', 'THRESHOLD',
                   'valid', 'data'
                   ]
        return objects.__iter__()

    def __str__(self):
        return f"DATA_W = {self.DATA_W}\n" + \
                f"THRESHOLD = {self.THRESHOLD}\n" + \
                f"valid = {self.valid}\n" + \
                f"data = {self.data}\n"


class SeqItemOut(SeqItem):

    def __init__(self):
        super().__init__()
        self.overflow = 0

    def __iter__(self):
        objects = [ 'valid', 'data', 'overflow']
        return objects.__iter__()

    def __str__(self):
        return f"valid = {self.valid}\n" + \
                f"data = {self.data}\n" + \
                f"overflow = {self.overflow}\n"