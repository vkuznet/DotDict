#!/usr/bin/env python
#pylint: disable-msg=C0301,C0103

"""
Unit test for DotDict module
"""

import os
import sys
import unittest
from ddict import DotDict

class Test_DotDict(unittest.TestCase):
    """
    A test class for the DotDict module
    """
    def setUp(self):
        """
        set up DAS core module
        """
        self.rec1 = {'a':{'b':1, 'c':[1,2]}}
        self.rec2 = {'a':[{'b':1, 'c':[1,2]}, {'b':10, 'c':[10,20]}]}

    def test_get_keys(self):
        """test get_keys method"""
        rec = DotDict(self.rec1)
        expect = ['a', 'a.b', 'a.c']
        expect.sort()
        result = rec.get_keys()
        result.sort()
        self.assertEqual(expect, result)

        rec = DotDict(self.rec2)
        result = rec.get_keys()
        result.sort()
        self.assertEqual(expect, result)

    def test_get(self):
        """test get method"""
        rec = DotDict(self.rec1)
        expect = [1,2]
        result = rec.get('a.c')
        self.assertEqual(expect, result)
        self.assertEqual(expect, rec['a.c'])

    def test_get_values(self):
        """test get_values method"""
        rec = DotDict(self.rec2)
        expect = [1, 2, 10, 20]
        result = [o for o in rec.get_values('a.c')]
        self.assertEqual(expect, result)

    def test_set(self):
        """test set method"""
        rec = DotDict(self.rec1)
        rec['a.d'] = 111
        self.assertEqual(rec['a.d'], 111)
        self.assertRaises(Exception, rec.set, ('a.c.d', 1))

    def test_delete(self):
        """test delete method"""
        rec = DotDict(self.rec1)
        rec.delete('a.c')
        expect = {'a':{'b':1}}
        self.assertEqual(expect, rec)

    def test_DotDict(self):
        """Test DotDict class"""
        res = {u'zip' : {u'code':u'14850'}}
        mdict = DotDict(res)
        mdict['zip.code'] = 14850
        expect = {u'zip' : {u'code':14850}}
        self.assertEqual(expect, mdict)

        res = {'a':{'b':{'c':10}, 'd':10}}
        mdict = DotDict(res)
        mdict['x.y.z'] = 10
        expect = {'a':{'b':{'c':10}, 'd':10}, 'x':{'y':{'z':10}}}
        self.assertEqual(expect, mdict)

        mdict['a.b.k.m'] = 10
        expect = {'a':{'b':{'c':10, 'k':{'m':10}}, 'd':10}, 'x':{'y':{'z':10}}}
        self.assertEqual(expect, mdict)
        expect = 10
        result = mdict.get('a.b.k.m')
        self.assertEqual(expect, result)

        res = {'a':{'b':{'c':10}, 'd':[{'x':1}, {'x':2}]}}
        mdict = DotDict(res)
        expect = 1
        result = mdict.get('a.d.x')
        self.assertEqual(expect, result)
        expect = None
        result = mdict.get('a.M.Z')
        self.assertEqual(expect, result)

        res = {'a': {'b': {'c':1, 'd':2}}}
        mdict = DotDict(res)
        expect = {'a': {'b': {'c':1}}}
        mdict.delete('a.b.d')
        self.assertEqual(expect, mdict)

    def test_DotDict_list(self):
        """Test DotDict class"""
        res = {'a':[{'b':1, 'c':1}, {'c':1}]}
        mdict = DotDict(res)
        expect = 1
        result = mdict.get('a.b')
        self.assertEqual(expect, result)

        res = {'a':[{'c':1}, {'b':1, 'c':1}]}
        mdict = DotDict(res)
        expect = 1
        result = mdict.get('a.b')
        self.assertEqual(expect, result)

    def test_DotDict_values(self):
        """Test DotDict get_values method"""
        res = {'a':[{'b':1, 'c':1}, {'c':2}]}
        mdict = DotDict(res)
        expect = [1]
        result = [r for r in mdict.get_values('a.b')]
        self.assertEqual(expect, result)
        
        expect = [1,2]
        result = [r for r in mdict.get_values('a.c')]
        self.assertEqual(expect, result)
        
        res = {'a':[{'b': [{'c':2}, {'c':3}]}, {'b': [{'c':4}, {'c':5}]}]}
        mdict = DotDict(res)
        expect = [2,3,4,5]
        result = [r for r in mdict.get_values('a.b.c')]
        self.assertEqual(expect, result)
        
    def test_DotDict_keys(self):
        """Test DotDict get_keys method"""
        res = {'a':[{'b':1, 'c':1}, {'c':2}]}
        mdict = DotDict(res)
        expect = ['a.b', 'a.c']
        result = [r for r in mdict.get_keys('a')]
        self.assertEqual(set(expect), set(result))

        res = {'a':[{'b': [{'c':2}, {'c':{'d':1}}]},
                    {'b': [{'c':4}, {'c':5}]}]}
        mdict = DotDict(res)
        expect = ['a.b', 'a.b.c', 'a.b.c.d']
        result = [r for r in mdict.get_keys('a')]
        self.assertEqual(set(expect), set(result))
#
# main
#
if __name__ == '__main__':
    unittest.main()

