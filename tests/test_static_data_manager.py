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
obj = query_content.StaticDataManager(fabric())


class TestStaticDataManager(unittest.TestCase):
    def test_as_generator_of_dictionaries(self):
        res = obj.as_generator_of_dictionaries("select * from lorem_cross.city")
        self.assertTrue(hasattr(res, 'next'))

    def test_as_dictionaries(self):
        res = obj.as_dictionaries(False, "select * from lorem_cross.city")
        self.assertTrue((isinstance(res, list) and isinstance(res[0], dict)))

    def test_as_empty_dictionaries(self):
        self.assertRaises(custom_errors.DataError, obj.as_dictionaries,
                          True, "select * from lorem_cross.city where id = -100500")

    def test_as_dictionary(self):
        res = obj.as_dictionary(False, "select * from lorem_cross.city limit 1")
        self.assertTrue(res, dict)

    def test_as_empty_dictionary(self):
        self.assertRaises(custom_errors.DataError, obj.as_dictionary,
                          True, "select * from lorem_cross.city where id = -100500")

    def test_as_generator_of_tuples(self):
        res = obj.as_generator_of_tuples("select * from lorem_cross.city")
        self.assertTrue(hasattr(res, 'next'))

    def test_as_tuples(self):
        res = obj.as_tuples(False, "select * from lorem_cross.city")
        self.assertTrue((isinstance(res, list) and isinstance(res[0], tuple)))

    def test_as_empty_tuples(self):
        self.assertRaises(custom_errors.DataError, obj.as_tuples,
                          True, "select * from lorem_cross.city where id = -100500")

    def test_as_tuple(self):
        res = obj.as_tuple(False, "select * from lorem_cross.city")
        self.assertTrue(isinstance(res, tuple))

    def test_as_empty_tuple(self):
        self.assertRaises(custom_errors.DataError, obj.as_tuple,
                          True, "select * from lorem_cross.city where id = -100500")

    def test_as_value(self):
        res = obj.as_value(False, "select id from lorem_cross.city")
        self.assertTrue(isinstance(res, int))

    def test_as_empty_value(self):
        self.assertRaises(custom_errors.DataError, obj.as_value,
                          True, "select id from lorem_Cross.city where id = -100500")


class TestStaticDataWrapper(unittest.TestCase):
    def test_generator_of_dictionaries(self):
        @obj.generator_of_dictionaries("select * from lorem_cross.city")
        def run(*_, **kwargs):
            return kwargs['result']
        res = run()
        self.assertTrue(hasattr(res, 'next'))

    def test_dictionaries(self):
        @obj.dictionaries("select * from lorem_cross.city")
        def run(*_, **kwargs):
            return kwargs['result']
        res = run()
        self.assertTrue((isinstance(res, list) and isinstance(res[0], dict)))

    def test_empty_dictionaries(self):
        @obj.dictionaries("select * from lorem_cross.city where id = -100500", look4empty=True)
        def run(*_, **kwargs):
            return kwargs['result']
        self.assertRaises(custom_errors.DataError, run)

    def test_dictionary(self):
        @obj.dictionary("select * from lorem_cross.city limit 1")
        def run(*_, **kwargs):
            return kwargs['result']
        res = run()
        self.assertTrue(res, dict)

    def test_empty_dictionary(self):
        @obj.dictionary("select * from lorem_cross.city where id = -100500", look4empty=True)
        def run(*_, **kwargs):
            return kwargs['result']
        self.assertRaises(custom_errors.DataError, run)

    def test_generator_of_tuples(self):
        @obj.generator_of_tuples("select * from lorem_cross.city")
        def run(*_, **kwargs):
            return kwargs['result']
        res = run()
        self.assertTrue(hasattr(res, 'next'))

    def test_tuples(self):
        @obj.tuples("select * from lorem_cross.city")
        def run(*_, **kwargs):
            return kwargs['result']
        res = run()
        self.assertTrue((isinstance(res, list) and isinstance(res[0], tuple)))

    def test_empty_tuples(self):
        @obj.tuples("select * from lorem_cross.city where id = -100500", look4empty=True)
        def run(*_, **kwargs):
            return kwargs['result']
        self.assertRaises(custom_errors.DataError, run)

    def test_tuple(self):
        @obj.tuple("select * from lorem_cross.city")
        def run(*_, **kwargs):
            return kwargs['result']
        res = run()
        self.assertTrue(isinstance(res, tuple))

    def test_empty_tuple(self):
        @obj.tuple("select * from lorem_cross.city where id = -100500", look4empty=True)
        def run(*_, **kwargs):
            return kwargs['result']
        self.assertRaises(custom_errors.DataError, run)

    def test_value(self):
        @obj.value("select id from lorem_cross.city")
        def run(*_, **kwargs):
            return kwargs['result']
        res = run()
        self.assertTrue(isinstance(res, int))

    def test_empty_value(self):
        @obj.value("select id from lorem_Cross.city where id = -100500", look4empty=True)
        def run(*_, **kwargs):
            return kwargs['result']
        self.assertRaises(custom_errors.DataError, run)


class TestStaticWrapInstance(unittest.TestCase):
    def test_generator_of_dictionaries(self):
        class Cls:
            @obj.generator_of_dictionaries("select * from lorem_cross.city")
            def run(self, *_, **kwargs):
                return kwargs['result']
        res = Cls().run()
        self.assertTrue(hasattr(res, 'next'))

    def test_dictionaries(self):
        class Cls:
            @obj.dictionaries("select * from lorem_cross.city")
            def run(self, *_, **kwargs):
                return kwargs['result']
        res = Cls().run()
        self.assertTrue((isinstance(res, list) and isinstance(res[0], dict)))

    def test_empty_dictionaries(self):
        class Cls:
            @obj.dictionaries("select * from lorem_cross.city where id = -100500", look4empty=True)
            def run(self, *_, **kwargs):
                return kwargs['result']
        self.assertRaises(custom_errors.DataError, Cls().run)

    def test_dictionary(self):
        class Cls:
            @obj.dictionary("select * from lorem_cross.city limit 1")
            def run(self, *_, **kwargs):
                return kwargs['result']
        res = Cls().run()
        self.assertTrue(res, dict)

    def test_empty_dictionary(self):
        class Cls:
            @obj.dictionary("select * from lorem_cross.city where id = -100500", look4empty=True)
            def run(self, *_, **kwargs):
                return kwargs['result']
        self.assertRaises(custom_errors.DataError, Cls().run)

    def test_generator_of_tuples(self):
        class Cls:
            @obj.generator_of_tuples("select * from lorem_cross.city")
            def run(self, *_, **kwargs):
                return kwargs['result']
        res = Cls().run()
        self.assertTrue(hasattr(res, 'next'))

    def test_tuples(self):
        class Cls:
            @obj.tuples("select * from lorem_cross.city")
            def run(self, *_, **kwargs):
                return kwargs['result']
        res = Cls().run()
        self.assertTrue((isinstance(res, list) and isinstance(res[0], tuple)))

    def test_empty_tuples(self):
        class Cls:
            @obj.tuples("select * from lorem_cross.city where id = -100500", look4empty=True)
            def run(self, *_, **kwargs):
                return kwargs['result']
        self.assertRaises(custom_errors.DataError, Cls().run)

    def test_tuple(self):
        class Cls:
            @obj.tuple("select * from lorem_cross.city")
            def run(self, *_, **kwargs):
                return kwargs['result']
        res = Cls().run()
        self.assertTrue(isinstance(res, tuple))

    def test_empty_tuple(self):
        class Cls:
            @obj.tuple("select * from lorem_cross.city where id = -100500", look4empty=True)
            def run(self, *_, **kwargs):
                return kwargs['result']
        self.assertRaises(custom_errors.DataError, Cls().run)

    def test_value(self):
        class Cls:
            @obj.value("select id from lorem_cross.city")
            def run(self, *_, **kwargs):
                return kwargs['result']
        res = Cls().run()
        self.assertTrue(isinstance(res, int))

    def test_empty_value(self):
        class Cls:
            @obj.value("select id from lorem_Cross.city where id = -100500", look4empty=True)
            def run(self, *_, **kwargs):
                return kwargs['result']
        self.assertRaises(custom_errors.DataError, Cls().run)

if __name__ == '__main__':
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestStaticDataManager)
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestStaticDataWrapper)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStaticWrapInstance)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
