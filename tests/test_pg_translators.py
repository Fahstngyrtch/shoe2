# -*- coding: utf-8 -*-
import os
import sys
import unittest
from decimal import Decimal
import uuid

from translators import PgBool, PgInt2, PgInt4, PgInt8, PgDate, PgTime
from translators import PgDateTime, PgInterval, PgJSON, PgFloatDouble, PgString
from translators import PgFloatNumeric, PgDecimalDouble, PgDecimalNumeric
from translators import PgText, PgGUID, PgSafeString

BASEDIR = os.path.dirname(os.path.abspath(__file__)) + "{0}..{0}".format(os.sep)
sys.path.append(BASEDIR)


class TestPgTranslators(unittest.TestCase):
    def test_format_bool_true(self):
        b = PgBool(True)
        expr = "{0}".format(b)
        self.assertEqual(expr, "True")
        
    def test_format_bool_false(self):
        b = PgBool(False)
        expr = "{0}".format(b)
        self.assertEqual(expr, "False")
    
    def test_format_bool_none(self):
        b = PgBool(None)
        expr = "{0}".format(b)
        self.assertEqual(expr, 'NULL::boolean')
    
    def test_format_int2(self):
        i2 = PgInt2(14)
        expr = "{0}".format(i2)
        self.assertEqual(expr, '14::int2')
    
    def test_format_int2_none(self):
        i2 = PgInt2(None)
        expr = "{0}".format(i2)
        self.assertEqual(expr, 'NULL::int2')
    
    def test_format_wrong_int2(self):
        self.assertRaises(ValueError, PgInt2, "ABC")
        
    def test_format_int2_overflowed(self):
        self.assertRaises(ValueError, PgInt2, 1000000000)
    
    def test_format_int4(self):
        i4 = PgInt4(180000)
        expr = "{0}".format(i4)
        self.assertEqual(expr, "180000::int4")
    
    def test_format_int4_none(self):
        i4 = PgInt4(None)
        expr = "{0}".format(i4)
        self.assertEqual(expr, 'NULL::int4')
    
    def test_format_wrong_int4(self):
        self.assertRaises(ValueError, PgInt4, "ABC")
    
    def test_format_int8(self):
        i8 = PgInt8(400000000000)
        expr = "{0}".format(i8)
        self.assertEqual(expr, "400000000000::int8")
    
    def test_format_int8_none(self):
        i8 = PgInt8(None)
        expr = "{0}".format(i8)
        self.assertEqual(expr, 'NULL::int8')
    
    def test_format_wrong_int8(self):
        self.assertRaises(ValueError, PgInt8, "ABC")
        
    def test_format_float_double(self):
        fd = PgFloatDouble(14.839)
        expr = "{0}".format(fd)
        self.assertEqual(expr, "14.839::double")
        
    def test_format_float_double_none(self):
        fd = PgFloatDouble(None)
        expr = "{0}".format(fd)
        self.assertEqual(expr, 'NULL::double')
        
    def test_format_float_double_wrong(self):
        self.assertRaises(ValueError, PgFloatDouble, "ABC")

    def test_format_float_double_sized(self):
        fd = PgFloatDouble(2)
        expr = "{0}".format(fd(14.839))
        self.assertEqual(expr, "14.84::double")
        
    def test_format_float_double_none_sized(self):
        fd = PgFloatDouble(2)
        expr = "{0}".format(fd(None))
        self.assertEqual(expr, 'NULL::double')
        
    def test_format_float_double_wrong_sized(self):
        fd = PgFloatDouble(2)
        self.assertRaises(ValueError, fd, "ABC")

    def test_format_float_numeric(self):
        fn = PgFloatNumeric(14.839)
        expr = "{0}".format(fn)
        self.assertEqual(expr, '14.839::numeric')
        
    def test_format_float_numeric_none(self):
        fn = PgFloatNumeric(None)
        expr = "{0}".format(fn)
        self.assertEqual(expr, 'NULL::numeric')
        
    def test_format_float_numeric_wrong(self):
        self.assertRaises(ValueError, PgFloatNumeric, "ABC")
        
    def test_format_float_numeric_sized(self):
        fn = PgFloatNumeric(2)
        expr = "{0}".format(fn(14.839))
        self.assertEqual(expr, "14.84::numeric")
        
    def test_format_float_numeric_none_sized(self):
        fn = PgFloatNumeric(2)
        expr = "{0}".format(fn(None))
        self.assertEqual(expr, 'NULL::numeric')
        
    def test_format_float_numeric_wrong_sized(self):
        fn = PgFloatNumeric(2)
        self.assertRaises(ValueError, fn, "ABC")

    def test_format_decimal_double(self):
        dd = PgDecimalDouble(Decimal('14.839'))
        expr = "{0}".format(dd)
        self.assertEqual(expr, '14.839::double')
        
    def test_format_decimal_double_none(self):
        dd = PgDecimalDouble(None)
        expr = "{0}".format(dd)
        self.assertEqual(expr, 'NULL::double')
        
    def test_format_decimal_double_wrong(self):
        self.assertRaises(ValueError, PgDecimalDouble, "ABC")

    def test_format_decimal_double_sized(self):
        dd = PgDecimalDouble(2)
        expr = "{0}".format(dd(Decimal('14.839')))
        self.assertEqual(expr, '14.84::double')
        
    def test_format_decimal_double_none_sized(self):
        dd = PgDecimalDouble(2)
        expr = "{0}".format(dd(None))
        self.assertEqual(expr, 'NULL::double')
        
    def test_format_decimal_double_wrong_sized(self):
        dd = PgDecimalDouble(2)
        self.assertRaises(ValueError, dd, "ABC")

    def test_format_decimal_numeric(self):
        dn = PgDecimalNumeric(Decimal('14.839'))
        expr = "{0}".format(dn)
        self.assertEqual(expr, '14.839::numeric')
        
    def test_format_decimal_numeric_none(self):
        dn = PgDecimalNumeric(None)
        expr = "{0}".format(dn)
        self.assertEqual(expr, 'NULL::numeric')
        
    def test_format_decimal_numeric_wrong(self):
        self.assertRaises(ValueError, PgDecimalNumeric, "ABC")
        
    def test_format_decimal_numeric_sized(self):
        dn = PgDecimalNumeric(2)
        expr = "{0}".format(dn(Decimal('14.839')))
        self.assertEqual(expr, '14.84::numeric')
        
    def test_format_decimal_numeric_none_sized(self):
        dn = PgDecimalNumeric(2)
        expr = "{0}".format(dn(None))
        self.assertEqual(expr, 'NULL::numeric')
        
    def test_format_decimal_numeric_wrong_sized(self):
        dn = PgDecimalNumeric(2)
        self.assertRaises(ValueError, dn, "ABC")
        
    def test_format_string(self):
        s = PgString("Абвгд")
        expr = "{0}".format(s)
        self.assertEqual(expr, "'Абвгд'::varchar")
    
    def test_format_string_empty(self):
        s = PgString(None)
        expr = "{0}".format(s)
        self.assertEqual(expr, 'NULL::varchar')
        
    def test_format_string_of_wrong_coding(self):
        s = PgString(u"Абвгд")
        expr = "{0}".format(s)
        self.assertEqual(expr, "'Абвгд'::varchar")
        
    def test_format_string_sized(self):
        s = PgString(3)
        expr = "{0}".format(s("Абвгд"))
        self.assertEqual(expr, "'Абв'::varchar")
        
    def test_format_string_sized_empty(self):
        s = PgString(3)
        expr = "{0}".format(s(None))
        self.assertEqual(expr, 'NULL::varchar')
        
    def test_format_string_sized_of_wrong_coding(self):
        s = PgString(3)
        expr = "{0}".format(s(u"Абвгд"))
        self.assertEqual(expr, "'Абв'::varchar")

    def test_format_safe_string(self):
        ss = PgSafeString("$Abcde;")
        expr = "{0}".format(ss)
        self.assertEqual(expr, "'Abcde'::varchar")
    
    def test_format_safe_string_empty(self):
        ss = PgSafeString(None)
        expr = "{0}".format(ss)
        self.assertEqual(expr, 'NULL::varchar')
        
    def test_format_safe_string_of_wrong_coding(self):
        ss = PgSafeString(u"Абвгд")
        expr = "{0}".format(ss)
        self.assertEqual(expr, "'Абвгд'::varchar")
        
    def test_format_safe_string_sized(self):
        ss = PgSafeString(3)
        expr = "{0}".format(ss("$Abcde;"))
        self.assertEqual(expr, "'Abc'::varchar")
        
    def test_format_safe_string_sized_empty(self):
        ss = PgSafeString(3)
        expr = "{0}".format(ss(None))
        self.assertEqual(expr, 'NULL::varchar')
        
    def test_format_safe_string_sized_of_wrong_coding(self):
        ss = PgSafeString(3)
        expr = "{0}".format(ss(u"Абвгд"))
        self.assertEqual(expr, "'Абв'::varchar")

    def test_format_date(self):
        d = PgDate("04.08.2016")
        expr = "{0}".format(d)
        self.assertEqual(expr, "'04.08.2016'::date")
    
    def test_format_date_none(self):
        d = PgDate(None)
        expr = "{0}".format(d)
        self.assertEqual(expr, 'NULL::date')
    
    def test_format_wrong_date(self):
        self.assertRaises(ValueError, PgDate, "Abcde")
    
    def test_format_time(self):
        t = PgTime("22:14:08")
        expr = "{0}".format(t)
        self.assertEqual(expr, "'22:14:08'::time")
    
    def test_format_wrong_time(self):
        self.assertRaises(ValueError, PgTime, "Abcde")
    
    def test_format_time_none(self):
        t = PgTime(None)
        expr = "{0}".format(t)
        self.assertEqual(expr, 'NULL::time')
    
    def test_format_datetime(self):
        dt = PgDateTime("13.09.1978 22:30")
        expr = "{0}".format(dt)
        self.assertEqual(expr, "'13.09.1978 22:30:00'::timestamp")
    
    def test_format_datetime_wrong(self):
        self.assertRaises(ValueError, PgDateTime, "7654321")
    
    def test_format_datetime_null(self):
        dt = PgDateTime(None)
        expr = "{0}".format(dt)
        self.assertEqual(expr, 'NULL::timestamp')
    
    def test_format_interval(self):
        i = PgInterval("1 day")
        expr = "{0}".format(i)
        self.assertEqual(expr, "'86400 second'::interval")
    
    def test_format_interval_wrong(self):
        self.assertRaises(ValueError, PgInterval, "Dddddddd")
    
    def test_format_interval_null(self):
        i = PgInterval(None)
        expr = "{0}".format(i)
        self.assertEqual(expr, 'NULL::interval')
    
    def test_format_text(self):
        t = PgText(u"Some text")
        expr = "{0}".format(t)
        self.assertEqual(expr, "'Some text'::text")
    
    def test_format_text_null(self):
        t = PgText(None)
        expr = "{0}".format(t)
        self.assertEqual(expr, 'NULL::text')
    
    def test_format_json(self):
        js = PgJSON({"Foo": "bar"})
        expr = "{0}".format(js)
        self.assertEqual(expr, """'{"Foo": "bar"}'::jsonb""")
    
    def test_format_json_null(self):
        js = PgJSON(None)
        expr = "{0}".format(js)
        self.assertEqual(expr, 'NULL::jsonb')
    
    def test_format_json_wrong(self):
        self.assertRaises(ValueError, PgJSON, "Not JSON")

    def test_format_guid(self):
        uid = uuid.uuid4()
        expr = "{0}".format(PgGUID(uid))
        self.assertEqual(expr, "'{0}'::guid".format(uid))

    def test_format_guid_null(self):
        uid = PgGUID(None)
        expr = "{0}".format(uid)
        self.assertEqual(expr, 'NULL::guid')

    def test_format_guid_wrong(self):
        self.assertRaises(ValueError, PgGUID, "Not UUID")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPgTranslators)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
