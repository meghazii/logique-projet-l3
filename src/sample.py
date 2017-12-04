class Operande(object):

    def __init__(self, s, b):
        self._symbole = s
        self._mini = b

    def setSym(self, s):
        self._symbole = s

    def Sym(self):
        return self._symbole

    def setMin(self, b):
        self._mini = b

    def mini(self):
        return self._mini

class Sym_Prop(object):

    def __init__(self, s):
        self._symbole = s


class Formule(object):

    def __init__(self, sym, ope):
        self._sym_l = sym
        self._ope_l = ope    
