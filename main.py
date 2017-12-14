"""!/usr/bin/python3.6
-*- coding: utf-8 -*-"""


class Operande(object):
    """Classe de operande, value reprensente les différentes operande
    1 = not, 2 = and, 3 = or, 4 = -> et 5 = <->"""
    def __init__(self, o_value):
        if o_value > 5 or o_value < 1:
            print("Erreur 1")
        else:
            self.value = o_value

    def getValue(self):
        return self.value

    def getChar(self):
        if self.value == 1:
            return "¬"
        elif self.value == 2:
            return "∧"
        elif self.value == 3:
            return "∨"
        elif self.value == 4:
            return "→"
        elif self.value == 5:
            return "↔"

    def inverse(self):
        if (self.value == 3):
            self.value = 2
        elif (self.value == 2):
            self.value = 3


class Symbole(object):
    """ Classe pour les symboles propositionnel"""
    def __init__(self, s_char):
        self.char = s_char

    def getSym(self):
        return self.char

    def afficher_sym(self):
        print(self.char)


class Mot(object):

    def __init__(self, obj, m_minimal, no=False, ope=None, m2=None):
        self.minimal = m_minimal
        self.operande = ope
        self.mot1 = obj
        self.no = no
        if (self.no):
            self.noSym = Operande(1)
        if (not self.minimal):
            self.mot2 = m2

    def inverse(self):
        self.setNo(not self.no)
        self.mot1.setNo(not self.mot1.getNo())
        self.mot2.setNo(not self.mot2.getNo())
        self.operande.inverse()

    def getNo(self):
        return self.no

    def setNo(self, b):
        self.no = b
        if (b):
            self.noSym = Operande(1)
        else:
            self.noSyme = None

    def setM1(self, mot):
        self.mot1 = mot

    def getM1(self):
        return self.mot1

    def setM2(self, mot):
        self.mot2 = mot

    def getM2(self):
        return self.mot2

    def setOp(self, ope):
        self.operande = ope

    def getOp(self):
        return self.operande

    def getMin(self):
        return self.minimal

    def afficher_mot(self):
        if (self.minimal):
            if (self.no):
                a = self.noSym.getChar() + self.mot1.getSym()
                return a
            else:
                a = self.mot1.getSym()
                return a
        else:
            if (self.no):
                a = self.noSym.getChar() + "(" + self.mot1.afficher_mot()
                a = a + self.operande.getChar()
                a = a + self.mot2.afficher_mot() + ")"
                return a
            else:
                a = "(" + self.mot1.afficher_mot()
                a = a + self.operande.getChar()
                a = a + self.mot2.afficher_mot() + ")"
                return a

    def simplify(self):
        notO = self.getNo()
        word1 = self.getM1()
        if (self.minimal):
            ope = self.operande.getValue()
        else:
            word2 = self.getM2()

        if (ope == 3 or ope == 2):
            if(word1.getMin() and word2.getMin() and notO):
                """ si les deux enfants sont min et neg on inverse"""
                self.inverse()

            elif (word1.getMin() or word2.getMin()):
                """ si au moins 1 des deux enfants sont minimum"""
                mini = None
                other = None
                if (word1.getMin()):
                    """ Si word1 est min"""
                    mini = word1
                    other = word2
                elif (word2.getMin()):
                    """ Si word2 est min"""
                    mini = word2
                    other = word1
                """ On applique la distributivité """
                op1 = word1.getOp().getValue()
                op2 = word2.getOp().getValue()
                m1 = Mot(mini, False, False, ope, other.getM1())
                m2 = Mot(mini, False, False, ope, other.getM2())
                self = Mot(m1, False, False, op2, m2)
                if (notO):
                    self.inverse()

            elif (ope == op1 and ope == op2 and notO):
                """ si aucun des enfants n'est mini et ont same operande
                et neg"""
                self.inverse()

        else:
            if (ope == 5):
                a1 = Mot(word1, False, False, Operande(4), word2)
                a2 = Mot(word2, False, False, Operande(4), word1)
                self.setM1(a1)
                self.setM2(a2)
                self.setOp(Operande(2))

            elif(ope == 4):
                if (word1.getMin()):
                    m1 = Mot(word1.getM1(), True,
                             not word1.getNo())
                else:
                    m1 = Mot(word1.getM1(), False,
                             not word1.getNo(), word1.getOp(),
                             word1.getM2())
                if (word2.getMin()):
                    m2 = Mot(word2.getM1(), True,
                             word2.getNo())
                else:
                    m2 = Mot(word2.getM1(), False,
                             word2.getNo(), word2.getOp(),
                             word2.getM2())
                self.setM1(m1)
                self.setM2(m2)
                self.setOp(Operande(3))


op1 = Operande(1)
op2 = Operande(2)
op3 = Operande(3)
op4 = Operande(4)
op5 = Operande(5)

sym1 = Symbole("p")
sym2 = Symbole("q")
sym3 = Symbole("r")

m1 = Mot(sym1, True, False)  # p
m2 = Mot(sym2, True, False)  # q
m3 = Mot(m1, False, False, op4, m2)  # p→q
m4 = Mot(m3, False, False, op4, m2)  # ((p→q)→q)
m5 = Mot(m1, False, False, op4, m4)  # Formule (1.) (p→((p→q)→q))


m6 = Mot(sym2, True, True)  # ¬q
m7 = Mot(m1, False, True, op4, m2)  # ¬(p→q)
m8 = Mot(m6, False, False, op4, m7)  # ¬q → ¬(p→q)
m9 = Mot(m1, False, False, op4, m8)  # (p→(¬q→¬(p→q)))


print(m9.afficher_mot())

m9.simplify()

print(m9.afficher_mot())
