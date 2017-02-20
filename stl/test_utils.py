import stl
import stl.utils
import pandas as pd
from nose2.tools import params
import unittest
from sympy import Symbol

ex1 = ("F[b?, 1]G[0, c?](x > a?)", {"a?", "b?", "c?"})
ex2 = ("G[0, c?](x > a?)", {"a?", "c?"})
ex3 = ("F[b?, 1]G[0, c?](x > a?)", {"a?", "b?", "c?"})

ex4 = ("F[b?, 1]G[0, c?](x > a?)", "F[2, 1]G[0, 3](x > 1)")
ex5 = ("G[0, c?](x > a?)", "G[0, 3](x > 1)")

val = {"a?": 1.0, "b?": 2.0, "c?": 3.0}

class TestSTLUtils(unittest.TestCase):
    @params(ex1, ex2, ex3)
    def test_param_lens(self, phi_str, params):
        phi = stl.parse(phi_str)
        self.assertEqual(set(map(str, stl.utils.param_lens(phi).get_all())), params)
        
    @params(ex4, ex5)
    def test_set_params(self, phi_str, phi2_str):
        phi = stl.parse(phi_str)
        phi2 = stl.parse(phi2_str)
        phi = stl.utils.set_params(phi, val)
        
        self.assertEqual(set(map(str, stl.utils.param_lens(phi).get_all())), set())
        self.assertEqual(phi, phi2)

    @params(("x > 5", 1), ("~(x)", 2), ("(F[0,1](x)) & (~(G[0, 2](y)))", 6))
    def test_walk(self, phi_str, l):
        self.assertEqual(l, len(list(stl.walk(stl.parse(phi_str)))))

    @params(([], False, False),([int], True, False), ([int, bool], True, True))
    def test_type_pred(self, types, b1, b2):
        pred = stl.utils.type_pred(*types)
        self.assertFalse(pred(None))
        self.assertEqual(pred(1), b1)
        self.assertEqual(pred(True), b2)

    def test_ast_lens(self):
        raise NotImplementedError


    def test_terms_lens(self):
        raise NotImplementedError


    def test_f_neg_or_canonical_form(self):
        raise NotImplementedError

    def test_to_from_mtl(self):
        raise NotImplementedError

    def test_get_polarity(self):
        raise NotImplementedError

    def test_canonical_polarity(self):
        raise NotImplementedError
