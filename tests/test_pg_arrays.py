# -*- coding: utf-8 -*-
import os
import sys
import unittest
from decimal import Decimal
import uuid

from translators import PgArray, PgBool, PgInt2, PgInt4, PgInt8, PgDate, PgTime
from translators import PgDateTime, PgInterval, PgJSON, PgFloatDouble, PgText
from translators import PgFloatNumeric, PgDecimalDouble, PgDecimalNumeric
from translators import PgGUID, PgSafeString, PgString

BASEDIR = os.path.dirname(os.path.abspath(__file__)) + "{0}..{0}".format(os.sep)
sys.path.append(BASEDIR)


class TestPgArrayOfTranslators(unittest.TestCase):
    def test_array_of_bool(self):
        b = PgArray(PgBool)([True, True, False])
        expr = "{0}".format(b)
        self.assertEqual(expr, "ARRAY[True,True,False]::boolean[]")

    def test_array_of_bool_none(self):
        b = PgArray(PgBool)(None)
        expr = "{0}".format(b)
        self.assertEqual(expr, 'ARRAY[NULL::boolean]::boolean[]')
    
    def test_array_of_int2(self):
        i2 = PgArray(PgInt2)([14, 22, 70])
        expr = "{0}".format(i2)
        self.assertEqual(expr, 'ARRAY[14::int2,22::int2,70::int2]::int2[]')
    
    def test_array_of_int2_none(self):
        i2 = PgArray(PgInt2)(None)
        expr = "{0}".format(i2)
        self.assertEqual(expr, 'ARRAY[NULL::int2]::int2[]')

    def test_array_of_int4(self):
        i4 = PgArray(PgInt4)([180000, 42, 300])
        expr = "{0}".format(i4)
        self.assertEqual(expr, "ARRAY[180000::int4,42::int4,300::int4]::int4[]")
    
    def test_array_of_int4_none(self):
        i4 = PgArray(PgInt4)(None)
        expr = "{0}".format(i4)
        self.assertEqual(expr, 'ARRAY[NULL::int4]::int4[]')

    def test_array_of_int8(self):
        i8 = PgArray(PgInt8)([400000000000, ])
        expr = "{0}".format(i8)
        self.assertEqual(expr, "ARRAY[400000000000::int8]::int8[]")
    
    def test_array_of_int8_none(self):
        i8 = PgArray(PgInt8)(None)
        expr = "{0}".format(i8)
        self.assertEqual(expr, 'ARRAY[NULL::int8]::int8[]')
    
    def test_array_of_float_double(self):
        fd = PgArray(PgFloatDouble)([14.839, 3.142])
        expr = "{0}".format(fd)
        self.assertEqual(expr, "ARRAY[14.839::double,3.142::double]::double[]")
        
    def test_array_of_float_double_none(self):
        fd = PgArray(PgFloatDouble)(None)
        expr = "{0}".format(fd)
        self.assertEqual(expr, 'ARRAY[NULL::double]::double[]')
        
    def test_array_of_float_double_sized(self):
        fd = PgArray(PgFloatDouble(2))
        expr = "{0}".format(fd([14.839, 3.142]))
        self.assertEqual(expr, "ARRAY[14.84::double,3.14::double]::double[]")
        
    def test_array_of_float_double_none_sized(self):
        fd = PgArray(PgFloatDouble(2))
        expr = "{0}".format(fd(None))
        self.assertEqual(expr, 'ARRAY[NULL::double]::double[]')
        
    def test_array_of_float_numeric(self):
        fn = PgArray(PgFloatNumeric)([14.839, 3.142])
        expr = "{0}".format(fn)
        self.assertEqual(expr, 'ARRAY[14.839::numeric,3.142::numeric]::numeric[]')
        
    def test_array_of_float_numeric_none(self):
        fn = PgArray(PgFloatNumeric)(None)
        expr = "{0}".format(fn)
        self.assertEqual(expr, 'ARRAY[NULL::numeric]::numeric[]')

    def test_array_of_float_numeric_sized(self):
        fn = PgArray(PgFloatNumeric(2))
        expr = "{0}".format(fn([14.839, 3.142]))
        self.assertEqual(expr, "ARRAY[14.84::numeric,3.14::numeric]::numeric[]")
        
    def test_array_of_float_numeric_none_sized(self):
        fn = PgArray(PgFloatNumeric(2))
        expr = "{0}".format(fn(None))
        self.assertEqual(expr, 'ARRAY[NULL::numeric]::numeric[]')
        
    def test_array_of_decimal_double(self):
        dd = PgArray(PgDecimalDouble)([Decimal('14.839'), Decimal('3.142')])
        expr = "{0}".format(dd)
        self.assertEqual(expr, 'ARRAY[14.839::double,3.142::double]::double[]')
        
    def test_array_of_decimal_double_none(self):
        dd = PgArray(PgDecimalDouble)(None)
        expr = "{0}".format(dd)
        self.assertEqual(expr, 'ARRAY[NULL::double]::double[]')

    def test_array_of_decimal_double_sized(self):
        dd = PgArray(PgDecimalDouble(2))
        expr = "{0}".format(dd([Decimal('14.839'), Decimal('3.142')]))
        self.assertEqual(expr, 'ARRAY[14.84::double,3.14::double]::double[]')
        
    def test_array_of_decimal_double_none_sized(self):
        dd = PgArray(PgDecimalDouble(2))
        expr = "{0}".format(dd(None))
        self.assertEqual(expr, 'ARRAY[NULL::double]::double[]')

    def test_array_of_decimal_numeric(self):
        dn = PgArray(PgDecimalNumeric)([Decimal('14.839'), Decimal('3.142')])
        expr = "{0}".format(dn)
        self.assertEqual(expr, 'ARRAY[14.839::numeric,3.142::numeric]::numeric[]')
        
    def test_array_of_decimal_numeric_none(self):
        dn = PgArray(PgDecimalNumeric)(None)
        expr = "{0}".format(dn)
        self.assertEqual(expr, 'ARRAY[NULL::numeric]::numeric[]')

    def test_array_of_decimal_numeric_sized(self):
        dn = PgArray(PgDecimalNumeric(2))
        expr = "{0}".format(dn([Decimal('14.839'), Decimal('3.142')]))
        self.assertEqual(expr, 'ARRAY[14.84::numeric,3.14::numeric]::numeric[]')
        
    def test_array_of_decimal_numeric_none_sized(self):
        dn = PgArray(PgDecimalNumeric(2))
        expr = "{0}".format(dn(None))
        self.assertEqual(expr, 'ARRAY[NULL::numeric]::numeric[]')

    def test_array_of_string(self):
        s = PgArray(PgString)(["Abcde", "Fghij"])
        expr = "{0}".format(s)
        self.assertEqual(expr, "ARRAY['Abcde'::varchar,'Fghij'::varchar]::varchar[]")
    
    def test_array_of_string_empty(self):
        s = PgArray(PgString)(None)
        expr = "{0}".format(s)
        self.assertEqual(expr, 'ARRAY[NULL::varchar]::varchar[]')

    def test_array_of_string_sized(self):
        s = PgArray(PgString(3))
        expr = "{0}".format(s(["Abcde", "Fghij"]))
        self.assertEqual(expr, "ARRAY['Abc'::varchar,'Fgh'::varchar]::varchar[]")
        
    def test_array_of_string_sized_empty(self):
        s = PgArray(PgString(3))
        expr = "{0}".format(s(None))
        self.assertEqual(expr, 'ARRAY[NULL::varchar]::varchar[]')

    def test_array_of_unicode(self):
        u = PgArray(PgString)([u"Abcde", u"Fghij"])
        expr = "{0}".format(u)
        self.assertEqual(expr, "ARRAY['Abcde'::varchar,'Fghij'::varchar]::varchar[]")

    def test_array_of_unicode_sized(self):
        u = PgArray(PgString(3))
        expr = "{0}".format(u([u"Abcde", u"Fghij"]))
        self.assertEqual(expr, "ARRAY['Abc'::varchar,'Fgh'::varchar]::varchar[]")
        
    def test_array_of_safe_string(self):
        ss = PgArray(PgSafeString)(["$Abcde;", "$Fghij;"])
        expr = "{0}".format(ss)
        self.assertEqual(expr, "ARRAY['Abcde'::varchar,'Fghij'::varchar]::varchar[]")
    
    def test_array_of_safe_string_empty(self):
        ss = PgArray(PgSafeString)(None)
        expr = "{0}".format(ss)
        self.assertEqual(expr, 'ARRAY[NULL::varchar]::varchar[]')

    def test_array_of_safe_string_sized(self):
        ss = PgArray(PgSafeString(3))
        expr = "{0}".format(ss(["$Abcde;", "$Fghij;"]))
        self.assertEqual(expr, "ARRAY['Abc'::varchar,'Fgh'::varchar]::varchar[]")
        
    def test_array_of_safe_string_sized_empty(self):
        ss = PgArray(PgSafeString(3))
        expr = "{0}".format(ss(None))
        self.assertEqual(expr, 'ARRAY[NULL::varchar]::varchar[]')

    def test_array_of_safe_unicode(self):
        su = PgArray(PgSafeString)([u"$Abcde;", u"$Fghij;"])
        expr = "{0}".format(su)
        self.assertEqual(expr, "ARRAY['Abcde'::varchar,'Fghij'::varchar]::varchar[]")

    def test_array_of_safe_unicode_sized(self):
        su = PgArray(PgSafeString(3))
        expr = "{0}".format(su([u"$Abcde;", u"$Fghij"]))
        self.assertEqual(expr, "ARRAY['Abc'::varchar,'Fgh'::varchar]::varchar[]")

    def test_array_of_date(self):
        d = PgArray(PgDate)(["04.08.2016", "04.08.2017"])
        expr = "{0}".format(d)
        self.assertEqual(expr, "ARRAY['04.08.2016'::date,'04.08.2017'::date]::date[]")
    
    def test_array_of_date_none(self):
        d = PgArray(PgDate)(None)
        expr = "{0}".format(d)
        self.assertEqual(expr, 'ARRAY[NULL::date]::date[]')

    def test_array_of_time(self):
        t = PgArray(PgTime)(["22:14:08", "13:02:10"])
        expr = "{0}".format(t)
        self.assertEqual(expr, "ARRAY['22:14:08'::time,'13:02:10'::time]::time[]")

    def test_array_of_time_none(self):
        t = PgArray(PgTime)(None)
        expr = "{0}".format(t)
        self.assertEqual(expr, 'ARRAY[NULL::time]::time[]')
    
    def test_array_of_datetime(self):
        dt = PgArray(PgDateTime)(["13.09.1978 22:30", "22.09.2010 17:15"])
        expr = "{0}".format(dt)
        self.assertEqual(expr, "ARRAY['13.09.1978 22:30:00'::timestamp,'22.09.2010 17:15:00'::timestamp]::timestamp[]")

    def test_array_of_datetime_null(self):
        dt = PgArray(PgDateTime)(None)
        expr = "{0}".format(dt)
        self.assertEqual(expr, 'ARRAY[NULL::timestamp]::timestamp[]')
    
    def test_array_of_interval(self):
        i = PgArray(PgInterval)(["1 day", "1 hour"])
        expr = "{0}".format(i)
        self.assertEqual(expr, "ARRAY['86400 second'::interval,'3600 second'::interval]::interval[]")

    def test_array_of_interval_null(self):
        i = PgArray(PgInterval)(None)
        expr = "{0}".format(i)
        self.assertEqual(expr, 'ARRAY[NULL::interval]::interval[]')
    
    def test_array_of_text(self):
        t = PgArray(PgText)([u"Some text", u"Another text"])
        expr = "{0}".format(t)
        self.assertEqual(expr, "ARRAY['Some text'::text,'Another text'::text]::text[]")
    
    def test_array_of_text_null(self):
        t = PgArray(PgText)(None)
        expr = "{0}".format(t)
        self.assertEqual(expr, 'ARRAY[NULL::text]::text[]')
    
    def test_array_of_json(self):
        js = PgArray(PgJSON)([{"Foo": "bar"}, {"Foo": "Baz"}])
        expr = "{0}".format(js)
        self.assertEqual(expr, """ARRAY['{"Foo": "bar"}'::jsonb,'{"Foo": "Baz"}'::jsonb]::jsonb[]""")
    
    def test_array_of_json_null(self):
        js = PgArray(PgJSON)(None)
        expr = "{0}".format(js)
        self.assertEqual(expr, 'ARRAY[NULL::jsonb]::jsonb[]')

    def test_array_of_guid(self):
        uid = uuid.uuid4()
        uid2 = uuid.uuid4()
        expr = "{0}".format(PgArray(PgGUID)([uid, uid2]))
        self.assertEqual(expr, "ARRAY['{0}'::guid,'{1}'::guid]::guid[]".format(uid, uid2))

    def test_array_of_guid_null(self):
        uid = PgArray(PgGUID)(None)
        expr = "{0}".format(uid)
        self.assertEqual(expr, 'ARRAY[NULL::guid]::guid[]')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPgArrayOfTranslators)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
