# -*- coding: utf-8 -*-
# TODO: create iso lens between sugar and non-sugar
# TODO: supress + given a + (-b). i.e. want a - b

from collections import namedtuple, deque
from itertools import repeat
from enum import Enum

import funcy as fn
from sympy import Symbol

dt_sym = Symbol('dt', positive=True)
t_sym = Symbol('t', positive=True)

def flatten_binary(phi):
    t = type(phi)
    f = lambda x: x.args if isinstance(x, t) else [x]
    return t(tuple(fn.mapcat(f, phi.args)))
        

class AST(object):
    def __or__(self, other):
        return flatten_binary(Or((self, other)))

    def __and__(self, other):
        return flatten_binary(And((self, other)))

    def __invert__(self):
        return Neg(self)



class AtomicPred(namedtuple("AP", ["id"]), AST):
    def __repr__(self):
        return "{}".format(self.id)

    def children(self):
        return []


class LinEq(namedtuple("LinEquality", ["terms", "op", "const"]), AST):
    def __repr__(self):
        return " + ".join(map(str, self.terms)) + f" {self.op} {self.const}"

    def children(self):
        return []


class Var(namedtuple("Var", ["coeff", "id", "time"])):
    def __repr__(self):
        return f"{self.coeff}*{self.id}[{self.time}]"


class Interval(namedtuple('I', ['lower', 'upper'])):
    def __repr__(self):
        return f"[{self.lower},{self.upper}]"

    def children(self):
        return [self.lower, self.upper]


class NaryOpSTL(namedtuple('NaryOp', ['args']), AST):
    OP = "?"
    def __repr__(self):
        return f" {self.OP} ".join(f"({x})" for x in self.args)

    def children(self):
        return self.args


class Or(NaryOpSTL):
    OP = "∨"

class And(NaryOpSTL):
    OP = "∧"


class ModalOp(namedtuple('ModalOp', ['interval', 'arg']), AST):
    def __repr__(self):
        return f"{self.OP}{self.interval}({self.arg})"
    
    def children(self):
        return [self.arg]


class F(ModalOp):
    OP = "◇"

class G(ModalOp):
    OP = "□"


class Neg(namedtuple('Neg', ['arg']), AST):
    def __repr__(self):
        return f"¬({self.arg})"

    def children(self):
        return [self.arg]
