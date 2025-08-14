class Stmp():

    ''' Our parser stamp '''
    def __init__(self):
        self.state = SL.INI
        self.scan = ()
        self.callf = None

    def call(self):
        ret = None
        if self.callf:
             ret = self.callf()
        return ret


