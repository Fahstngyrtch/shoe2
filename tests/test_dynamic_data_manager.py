# -*- coding: utf-8 -*-
import os
import sys
import unittest

BASEDIR = os.path.dirname(os.path.abspath(__file__)) + "{0}..{0}".format(os.sep)
sys.path.append(BASEDIR)

import psyco_connection
from connection import Capstone
import query_content
import custom_errors

fabric = Capstone(True, 'lorem_cross', 'lcadmin', 'Br@hec&^^', '127.0.0.1', 5432)
obj = query_content.DynamicDataManager(fabric())


class TestDynamicDataManager(unittest.TestCase):
    def test_as_generator_of_dictionaries(self):
        res = obj.as_generator_of_dictionaries('city', schema='lorem_cross')
        self.assertTrue(hasattr(res, 'next'))

    def test_as_dictionaries(self):
        res = obj.as_dictionaries('city', schema='lorem_cross')
        self.assertTrue((isinstance(res, list) and isinstance(res[0], dict)))

    def test_as_empty_dictionaries(self):
        self.assertRaises(custom_errors.DataError, obj.as_dictionaries,
                          'city', schema="lorem_cross", conditions={'id': ('=', -100500)}, look4empty=True)

    def test_as_dictionary(self):
        res = obj.as_dictionary('city', schema='lorem_cross')
        self.assertTrue(res, dict)

    def test_as_empty_dictionary(self):
        self.assertRaises(custom_errors.DataError, obj.as_dictionary,
                          'city', schema="lorem_cross", conditions={'id': ('=', -100500)}, look4empty=True)

    def test_as_generator_of_tuples(self):
        res = obj.as_generator_of_tuples('city', schema='lorem_cross')
        self.assertTrue(hasattr(res, 'next'))

    def test_as_tuples(self):
        res = obj.as_tuples('city', schema='lorem_cross')
        self.assertTrue((isinstance(res, list) and isinstance(res[0], tuple)))

    def test_as_empty_tuples(self):
        self.assertRaises(custom_errors.DataError, obj.as_tuples,
                          'city', schema="lorem_cross", conditions={'id': ('=', -100500)}, look4empty=True)

    def test_as_tuple(self):
        res = obj.as_tuple('city', schema='lorem_cross')
        self.assertTrue(isinstance(res, tuple))

    def test_as_empty_tuple(self):
        self.assertRaises(custom_errors.DataError, obj.as_tuple,
                          'city', schema="lorem_cross", conditions={'id': ('=', -100500)}, look4empty=True)

    def test_as_value(self):
        res = obj.as_value('city', schema='lorem_cross', items=['id', ])
        self.assertTrue(isinstance(res, int))

    def test_as_empty_value(self):
        self.assertRaises(custom_errors.DataError, obj.as_value,
                          'city', schema="lorem_cross", conditions={'id': ('=', -100500)}, look4empty=True)


class TestDynamicDataWrapper(unittest.TestCase):
    def test_generator_of_dictionaries(self):
        @obj.generator_of_dictionaries
        def run(*_, **kwargs):
            return kwargs['result']
        res = run('city', schema='lorem_cross')
        self.assertTrue(hasattr(res, 'next'))

    def test_dictionaries(self):
        @obj.dictionaries()
        def run(*_, **kwargs):
            return kwargs['result']
        res = run('city', schema='lorem_cross')
        self.assertTrue((isinstance(res, list) and isinstance(res[0], dict)))

    def test_empty_dictionaries(self):
        @obj.dictionaries(True)
        def run(*_, **kwargs):
            return kwargs['result']
        self.assertRaises(custom_errors.DataError, run, 'city', schema="lorem_cross",
                          conditions={'id': ('=', -100500)})

    def test_dictionary(self):
        @obj.dictionary()
        def run(*_, **kwargs):
            return kwargs['result']
        res = run('city', schema='lorem_cross')
        self.assertTrue(res, dict)

    def test_empty_dictionary(self):
        @obj.dictionary(look4empty=True)
        def run(*_, **kwargs):
            return kwargs['result']
        self.assertRaises(custom_errors.DataError, run, 'city', schema="lorem_cross", conditions={'id': ('=', -100500)})

    def test_generator_of_tuples(self):
        @obj.generator_of_tuples
        def run(*_, **kwargs):
            return kwargs['result']
        res = run('city', schema='lorem_cross')
        self.assertTrue(hasattr(res, 'next'))

    def test_tuples(self):
        @obj.tuples()
        def run(*_, **kwargs):
            return kwargs['result']
        res = run('city', schema='lorem_cross')
        self.assertTrue((isinstance(res, list) and isinstance(res[0], tuple)))

    def test_empty_tuples(self):
        @obj.tuples(look4empty=True)
        def run(*_, **kwargs):
            return kwargs['result']
        self.assertRaises(custom_errors.DataError, run, 'city', schema="lorem_cross", conditions={'id': ('=', -100500)})

    def test_tuple(self):
        @obj.tuple()
        def run(*_, **kwargs):
            return kwargs['result']
        res = run('city', schema='lorem_cross')
        self.assertTrue(isinstance(res, tuple))

    def test_empty_tuple(self):
        @obj.tuple(look4empty=True)
        def run(*_, **kwargs):
            return kwargs['result']
        self.assertRaises(custom_errors.DataError, run, 'city', schema="lorem_cross", conditions={'id': ('=', -100500)})

    def test_value(self):
        @obj.value()
        def run(*_, **kwargs):
            return kwargs['result']
        res = run('city', schema='lorem_cross', items=['id', ])
        self.assertTrue(isinstance(res, int))

    def test_empty_value(self):
        @obj.value(look4empty=True)
        def run(*_, **kwargs):
            return kwargs['result']
        self.assertRaises(custom_errors.DataError, run, 'city', schema="lorem_cross", conditions={'id': ('=', -100500)},
                          items=['id', ])


class TestDynamicWrapInstance(unittest.TestCase):
    def test_generator_of_dictionaries(self):
        class Cls:
            @obj.generator_of_dictionaries
            def run(self, *_, **kwargs):
                return kwargs['result']
        res = Cls().run('city', schema='lorem_cross')
        self.assertTrue(hasattr(res, 'next'))

    def test_dictionaries(self):
        class Cls:
            @obj.dictionaries()
            def run(self, *_, **kwargs):
                return kwargs['result']
        res = Cls().run('city', schema='lorem_cross')
        self.assertTrue((isinstance(res, list) and isinstance(res[0], dict)))

    def test_empty_dictionaries(self):
        class Cls:
            @obj.dictionaries(True)
            def run(self, *_, **kwargs):
                return kwargs['result']
        self.assertRaises(custom_errors.DataError, Cls().run, 'city', schema="lorem_cross",
                          conditions={'id': ('=', -100500)})

    def test_dictionary(self):
        class Cls:
            @obj.dictionary()
            def run(self, *_, **kwargs):
                return kwargs['result']
        res = Cls().run('city', schema='lorem_cross')
        self.assertTrue(res, dict)

    def test_empty_dictionary(self):
        class Cls:
            @obj.dictionary(look4empty=True)
            def run(self, *_, **kwargs):
                return kwargs['result']
        self.assertRaises(custom_errors.DataError, Cls().run,
                          'city', schema="lorem_cross", conditions={'id': ('=', -100500)})

    def test_generator_of_tuples(self):
        class Cls:
            @obj.generator_of_tuples
            def run(self, *_, **kwargs):
                return kwargs['result']
        res = Cls().run('city', schema='lorem_cross')
        self.assertTrue(hasattr(res, 'next'))

    def test_tuples(self):
        class Cls:
            @obj.tuples()
            def run(self, *_, **kwargs):
                return kwargs['result']
        res = Cls().run('city', schema='lorem_cross')
        self.assertTrue((isinstance(res, list) and isinstance(res[0], tuple)))

    def test_empty_tuples(self):
        class Cls:
            @obj.tuples(look4empty=True)
            def run(self, *_, **kwargs):
                return kwargs['result']
        self.assertRaises(custom_errors.DataError, Cls().run, 'city', schema="lorem_cross",
                          conditions={'id': ('=', -100500)})

    def test_tuple(self):
        class Cls:
            @obj.tuple()
            def run(self, *_, **kwargs):
                return kwargs['result']
        res = Cls().run('city', schema='lorem_cross')
        self.assertTrue(isinstance(res, tuple))

    def test_empty_tuple(self):
        class Cls:
            @obj.tuple(look4empty=True)
            def run(self, *_, **kwargs):
                return kwargs['result']
        self.assertRaises(custom_errors.DataError, Cls().run, 'city', schema="lorem_cross",
                          conditions={'id': ('=', -100500)})

    def test_value(self):
        class Cls:
            @obj.value()
            def run(self, *_, **kwargs):
                return kwargs['result']
        res = Cls().run('city', schema='lorem_cross', items=['id', ])
        self.assertTrue(isinstance(res, int))

    def test_empty_value(self):
        class Cls:
            @obj.value(look4empty=True)
            def run(self, *_, **kwargs):
                return kwargs['result']
        self.assertRaises(custom_errors.DataError, Cls().run, 'city', schema="lorem_cross",
                          conditions={'id': ('=', -100500)}, items=['id', ])

if __name__ == '__main__':
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestDynamicDataManager)
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestDynamicDataWrapper)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDynamicWrapInstance)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
