# -*- coding: utf-8 -*-
import os
import sys
import unittest
import datetime
import uuid

BASEDIR = os.path.dirname(os.path.abspath(__file__)) + "{0}..{0}".format(os.sep)
sys.path.append(BASEDIR)

import psyco_connection
from connection import Capstone
import query_content
import translators

fabric = Capstone(True, 'lorem_cross', 'lcadmin', 'Br@hec&^^', '127.0.0.1', 5432)
obj = query_content.DynamicDataManager(fabric())


class TestTranslateInputInCode(unittest.TestCase):
    def test_inputs_in_code(self):
        dt = datetime.date(2015, 9, 27)
        days = 2
        point = 7
        containers, values = (translators.PgDate, translators.PgInt4, translators.PgInt4), (dt, days, point)
        args = translators._translate(containers, values)
        res = obj.as_dictionaries("commgetregisters(%s,%s,%s)" % args, schema='lorem_cross')
        self.assertTrue(isinstance(res, list) and isinstance(res[0], dict))


class TestTranslateInputInFunction(unittest.TestCase):
    def test_inputs_in_function(self):
        @translators.translate(translators.PgDate, translators.PgInt4, translators.PgInt4)
        def make(dt, days, point):
            @obj.dictionaries()
            def run(*_, **kwargs):
                return kwargs['result']
            return run("commgetregisters(%s,%s,%s)" % (dt, days, point), schema='lorem_cross')

        res = make(datetime.date(2015, 9, 27), 2, 7)
        self.assertTrue(isinstance(res, list) and isinstance(res[0], dict))


class TestTranslateInputInInstance(unittest.TestCase):
    def test_inputs_in_instance(self):
        class Cls:
            @translators.translate(translators.PgDate, translators.PgInt4, translators.PgInt4)
            def make(self, dt, days, point):
                return self.run("commgetregisters(%s,%s,%s)" % (dt, days, point), schema='lorem_cross')

            @obj.dictionaries()
            def run(self, *_, **kwargs):
                return kwargs['result']

        res = Cls().make(datetime.date(2015, 9, 27), 2, 7)
        self.assertTrue(isinstance(res, list) and isinstance(res[0], dict))


class TestTranslateOutputInCode(unittest.TestCase):
    def test_dict_generator_with_simple_types(self):
        res = obj.as_generator_of_dictionaries(
            "passenger_bank", schema="control",
            conditions={"doc_date": ("is not", "null")},
            items=["id", "last_name", "first_name", "doc_date", "pass_type_id"])
        res = translators._retranslate({'id': translators.PtnInt8,
                                        'last_name': translators.PtnUnicode,
                                        'first_name': translators.PtnString,
                                        'doc_date': translators.PtnDate,
                                        'pass_type_id': translators.PtnInt4},
                                       res)
        res = res.next()
        self.assertTrue(all([isinstance(res['id'], long),
                             isinstance(res['last_name'], unicode),
                             isinstance(res['first_name'], str),
                             isinstance(res['doc_date'], datetime.date),
                             isinstance(res['pass_type_id'], int)]))

    def test_dict_list_with_simple_types(self):
        res = obj.as_dictionaries(
            "passenger_bank", schema="control",
            items=["id", "True as flag", "'1 day'::interval as inter"],
            conditions={"doc_date": ("is not", "null")})
        res = translators._retranslate({'id': translators.PtnInt8,
                                        'flag': translators.PtnBool,
                                        'inter': translators.PtnInterval},
                                       res)
        res = res[0]
        self.assertTrue(all([isinstance(res['id'], long),
                             isinstance(res['flag'], bool),
                             isinstance(res['inter'], datetime.timedelta)]))

    def test_dict_with_json(self):
        res = obj.as_dictionary("json_sample")
        res = translators._retranslate({'id': translators.PtnInt4,
                                        'data': translators.PtnJSON,
                                        'txt_data': translators.PtnUnicode},
                                       res)
        self.assertTrue(all([isinstance(res['id'], int),
                             isinstance(res['data'], dict),
                             isinstance(res['txt_data'], unicode)]))

    def test_tuple_generator_with_simple_types(self):
        res = obj.as_generator_of_tuples(
            "passenger_bank", schema="control",
            conditions={"doc_date": ("is not", "null")},
            items=["id", "last_name", "first_name", "doc_date", "pass_type_id"])
        res = translators._retranslate((translators.PtnInt8,
                                        translators.PtnUnicode,
                                        translators.PtnString,
                                        translators.PtnDate,
                                        translators.PtnInt4),
                                       res)
        res = res.next()
        self.assertTrue(all([isinstance(res[0], long),
                             isinstance(res[1], unicode),
                             isinstance(res[2], str),
                             isinstance(res[3], datetime.date),
                             isinstance(res[4], int)]))

    def test_tuple_list_with_simple_types(self):
        res = obj.as_tuples(
            "passenger_bank", schema="control",
            conditions={"doc_date": ("is not", "null")},
            items=["id", "True as flag", "'1 day'::interval as inter"])
        res = translators._retranslate((translators.PtnInt8,
                                        translators.PtnBool,
                                        translators.PtnInterval),
                                       res)
        res = res[0]
        self.assertTrue(all([isinstance(res[0], long),
                             isinstance(res[1], bool),
                             isinstance(res[2], datetime.timedelta)]))

    def test_tuple_with_json(self):
        res = obj.as_tuple("json_sample")
        res = translators._retranslate((translators.PtnInt4,
                                        translators.PtnJSON,
                                        translators.PtnUnicode),
                                       res)
        self.assertTrue(all([isinstance(res[0], int),
                             isinstance(res[1], dict),
                             isinstance(res[2], unicode)]))

    def test_value_with_guid(self):
        res = obj.as_value("generate_uuid()")
        res = translators._retranslate(translators.PtnGUID, res)
        self.assertIsInstance(res, uuid.UUID)


class TestTranslateOutputInFunction(unittest.TestCase):
    def test_dict_generator_with_simple_types(self):
        @obj.generator_of_dictionaries
        @translators.retranslate({'id': translators.PtnInt8,
                                  'last_name': translators.PtnUnicode,
                                  'first_name': translators.PtnString,
                                  'doc_date': translators.PtnDate,
                                  'pass_type_id': translators.PtnInt4})
        def run(*_, **kwargs):
            return kwargs['result']

        res = run("passenger_bank", schema="control",
                  conditions={"doc_date": ("is not", "null")},
                  items=["id", "last_name", "first_name",
                         "doc_date", "pass_type_id"]).next()
        self.assertTrue(all([isinstance(res['id'], long),
                             isinstance(res['last_name'], unicode),
                             isinstance(res['first_name'], str),
                             isinstance(res['doc_date'], datetime.date),
                             isinstance(res['pass_type_id'], int)]))

    def test_dict_list_with_simple_types(self):
        @obj.dictionaries()
        @translators.retranslate({'id': translators.PtnInt8,
                                  'flag': translators.PtnBool,
                                  'inter': translators.PtnInterval})
        def run(*_, **kwargs):
            return kwargs['result']
        res = run("passenger_bank", schema="control",
                  items=["id", "True as flag", "'1 day'::interval as inter"],
                  conditions={"doc_date": ("is not", "null")})[0]
        self.assertTrue(all([isinstance(res['id'], long),
                             isinstance(res['flag'], bool),
                             isinstance(res['inter'], datetime.timedelta)]))

    def test_dict_with_json(self):
        @obj.dictionary()
        @translators.retranslate({'id': translators.PtnInt4,
                                  'data': translators.PtnJSON,
                                  'txt_data': translators.PtnUnicode})
        def run(*_, **kwargs):
            return kwargs['result']

        res = run("json_sample")
        self.assertTrue(all([isinstance(res['id'], int),
                             isinstance(res['data'], dict),
                             isinstance(res['txt_data'], unicode)]))

    def test_tuple_generator_with_simple_types(self):
        @obj.generator_of_tuples
        @translators.retranslate((translators.PtnInt8,
                                  translators.PtnUnicode,
                                  translators.PtnString,
                                  translators.PtnDate,
                                  translators.PtnInt4))
        def run(*_, **kwargs):
            return kwargs['result']

        res = run("passenger_bank", schema="control",
                  conditions={"doc_date": ("is not", "null")},
                  items=["id", "last_name", "first_name",
                         "doc_date", "pass_type_id"]).next()
        self.assertTrue(all([isinstance(res[0], long),
                             isinstance(res[1], unicode),
                             isinstance(res[2], str),
                             isinstance(res[3], datetime.date),
                             isinstance(res[4], int)]))

    def test_tuple_list_with_simple_types(self):
        @obj.tuples()
        @translators.retranslate((translators.PtnInt8,
                                  translators.PtnBool,
                                  translators.PtnInterval))
        def run(*_, **kwargs):
            return kwargs['result']

        res = run("passenger_bank", schema="control",
                  conditions={"doc_date": ("is not", "null")},
                  items=["id", "True as flag", "'1 day'::interval as inter"])[0]
        self.assertTrue(all([isinstance(res[0], long),
                             isinstance(res[1], bool),
                             isinstance(res[2], datetime.timedelta)]))

    def test_tuple_with_json(self):
        @obj.tuple()
        @translators.retranslate((translators.PtnInt4,
                                  translators.PtnJSON,
                                  translators.PtnUnicode))
        def run(*_, **kwargs):
            return kwargs['result']

        res = run("json_sample")
        self.assertTrue(all([isinstance(res[0], int),
                             isinstance(res[1], dict),
                             isinstance(res[2], unicode)]))

    def test_value_with_guid(self):
        @obj.value()
        @translators.retranslate(translators.PtnGUID)
        def run(*_, **kwargs):
            return kwargs['result']

        res = run("generate_uuid()")
        self.assertIsInstance(res, uuid.UUID)


class TestTranslateOutputInInstasnce(unittest.TestCase):
    def test_dict_generator_with_simple_types(self):
        class Cls:
            @obj.generator_of_dictionaries
            @translators.retranslate({'id': translators.PtnInt8,
                                      'last_name': translators.PtnUnicode,
                                      'first_name': translators.PtnString,
                                      'doc_date': translators.PtnDate,
                                      'pass_type_id': translators.PtnInt4})
            def run(self, *_, **kwargs):
                return kwargs['result']

        res = Cls().run("passenger_bank", schema="control",
                        conditions={"doc_date": ("is not", "null")},
                        items=["id", "last_name", "first_name",
                               "doc_date", "pass_type_id"]).next()
        self.assertTrue(all([isinstance(res['id'], long),
                             isinstance(res['last_name'], unicode),
                             isinstance(res['first_name'], str),
                             isinstance(res['doc_date'], datetime.date),
                             isinstance(res['pass_type_id'], int)]))

    def test_dict_list_with_simple_types(self):
        class Cls:
            @obj.dictionaries()
            @translators.retranslate({'id': translators.PtnInt8,
                                      'flag': translators.PtnBool,
                                      'inter': translators.PtnInterval})
            def run(self, *_, **kwargs):
                return kwargs['result']
        res = Cls().run(
            "passenger_bank", schema="control",
            items=["id", "True as flag", "'1 day'::interval as inter"],
            conditions={"doc_date": ("is not", "null")})[0]
        self.assertTrue(all([isinstance(res['id'], long),
                             isinstance(res['flag'], bool),
                             isinstance(res['inter'], datetime.timedelta)]))

    def test_dict_with_json(self):
        class Cls:
            @obj.dictionary()
            @translators.retranslate({'id': translators.PtnInt4,
                                      'data': translators.PtnJSON,
                                      'txt_data': translators.PtnUnicode})
            def run(self, *_, **kwargs):
                return kwargs['result']

        res = Cls().run("json_sample")
        self.assertTrue(all([isinstance(res['id'], int),
                             isinstance(res['data'], dict),
                             isinstance(res['txt_data'], unicode)]))

    def test_tuple_generator_with_simple_types(self):
        class Cls:
            @obj.generator_of_tuples
            @translators.retranslate((translators.PtnInt8,
                                      translators.PtnUnicode,
                                      translators.PtnString,
                                      translators.PtnDate,
                                      translators.PtnInt4))
            def run(self, *_, **kwargs):
                return kwargs['result']

        res = Cls().run("passenger_bank", schema="control",
                        conditions={"doc_date": ("is not", "null")},
                        items=["id", "last_name", "first_name",
                               "doc_date", "pass_type_id"]).next()
        self.assertTrue(all([isinstance(res[0], long),
                             isinstance(res[1], unicode),
                             isinstance(res[2], str),
                             isinstance(res[3], datetime.date),
                             isinstance(res[4], int)]))

    def test_tuple_list_with_simple_types(self):
        class Cls:
            @obj.tuples()
            @translators.retranslate((translators.PtnInt8,
                                      translators.PtnBool,
                                      translators.PtnInterval))
            def run(self, *_, **kwargs):
                return kwargs['result']

        res = Cls().run("passenger_bank", schema="control",
                        conditions={"doc_date": ("is not", "null")},
                        items=["id", "True as flag",
                               "'1 day'::interval as inter"])[0]
        self.assertTrue(all([isinstance(res[0], long),
                             isinstance(res[1], bool),
                             isinstance(res[2], datetime.timedelta)]))

    def test_tuple_with_json(self):
        class Cls:
            @obj.tuple()
            @translators.retranslate((translators.PtnInt4,
                                      translators.PtnJSON,
                                      translators.PtnUnicode))
            def run(self, *_, **kwargs):
                return kwargs['result']

        res = Cls().run("json_sample")
        self.assertTrue(all([isinstance(res[0], int),
                             isinstance(res[1], dict),
                             isinstance(res[2], unicode)]))

    def test_value_with_guid(self):
        class Cls:
            @obj.value()
            @translators.retranslate(translators.PtnGUID)
            def run(self, *_, **kwargs):
                return kwargs['result']

        res = Cls().run("generate_uuid()")
        self.assertIsInstance(res, uuid.UUID)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTranslateInputInCode)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTranslateInputInFunction)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTranslateInputInInstance)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTranslateOutputInCode)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTranslateOutputInFunction)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTranslateOutputInInstasnce)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
