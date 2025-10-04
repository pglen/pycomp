class one():

    ''' Our parser stamp '''
    def __init__(self, val):
        self._data = ()
        self.val = val

    #def __repr__(self):
    #    return self

    def me(self):
        return str(self)

    def __str__(self):
        return str(self.val)

aa = one(1); bb = one(2)
bb = aa
#bb.__dict__ = aa.__dict__

print(id(aa), id(bb))
