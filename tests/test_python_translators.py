# -*- coding: utf-8 -*-
import os
import sys
import unittest
from decimal import Decimal
import uuid
import time
import datetime

from translators import PtnBool, PtnInt2, PtnInt4, PtnInt8, PtnDate, PtnTime
from translators import PtnFloat, PtnSizedFloat, PtnDecimal, PtnSizedDecimal
from translators import PtnString, PtnSizedString, PtnUnicode, PtnSizedUnicode
from translators import PtnJSON, PtnGUID, PtnDateTime, PtnInterval

BASEDIR = os.path.dirname(os.path.abspath(__file__)) + "{0}..{0}".format(os.sep)
sys.path.append(BASEDIR)


class TestPgTranslators(unittest.TestCase):
    def test_format_bool_true(self):
        b = PtnBool('t')
        self.assertEqual(b(), True)
        
    def test_format_bool_false(self):
        b = PtnBool('f')
        self.assertEqual(b(), False)
    
    def test_format_bool_none(self):
        b = PtnBool(None)
        self.assertIsNone(b())
    
    def test_format_int2(self):
        i2 = PtnInt2(14)
        self.assertEqual(i2(), 14)

    def test_format_int2_from_string(self):
        i2 = PtnInt2('14')
        self.assertEqual(i2(), 14)

    def test_format_int2_none(self):
        i2 = PtnInt2(None)
        self.assertIsNone(i2())
    
    def test_format_wrong_int2(self):
        self.assertRaises(ValueError, PtnInt2, "ABC")
    
    def test_format_int4(self):
        i4 = PtnInt4(180000)
        self.assertEqual(i4(), 180000)

    def test_format_int4_from_string(self):
        i4 = PtnInt4('180000')
        self.assertEqual(i4(), 180000)

    def test_format_int4_none(self):
        i4 = PtnInt4(None)
        self.assertIsNone(i4())
    
    def test_format_wrong_int4(self):
        self.assertRaises(ValueError, PtnInt4, "ABC")
    
    def test_format_int8(self):
        i8 = PtnInt8(400000000000)
        self.assertEqual(i8(), 400000000000)

    def test_format_int8_from_string(self):
        i8 = PtnInt8('400000000000')
        self.assertEqual(i8(), 400000000000)

    def test_format_int8_none(self):
        i8 = PtnInt8(None)
        self.assertIsNone(i8())
    
    def test_format_wrong_int8(self):
        self.assertRaises(ValueError, PtnInt8, "ABC")
        
    def test_format_float_from_float(self):
        fd = PtnFloat(14.839)
        self.assertEqual(fd(), 14.839)

    def test_format_float_from_decimal(self):
        fd = PtnFloat(Decimal('14.839'))
        self.assertEqual(fd(), 14.839)

    def test_format_float_from_string(self):
        fd = PtnFloat('14.839')
        self.assertEqual(fd(), 14.839)

    def test_format_float_none(self):
        fd = PtnFloat(None)
        self.assertIsNone(fd())
        
    def test_format_float_wrong(self):
        self.assertRaises(ValueError, PtnFloat, "ABC")

    def test_format_float_from_float_sized(self):
        fd = PtnSizedFloat(2)
        self.assertEqual(fd(14.839)(), 14.84)

    def test_format_float_from_decimal_sized(self):
        fd = PtnSizedFloat(1)
        self.assertEqual(fd(Decimal('14.839'))(), 14.8)

    def test_format_float_from_string_sized(self):
        fd = PtnSizedFloat(2)
        self.assertEqual(fd('14.839')(), 14.84)

    def test_format_float_none_sized(self):
        fd = PtnSizedFloat(1)
        self.assertIsNone(fd(None)())
        
    def test_format_float_wrong_sized(self):
        fd = PtnSizedFloat(2)
        self.assertRaises(ValueError, fd, "ABC")

    def test_format_decimal_from_float(self):
        dd = PtnDecimal(14.839)
        self.assertEqual(dd(), Decimal('14.839'))

    def test_format_decimal_from_decimal(self):
        dd = PtnDecimal(Decimal('14.839'))
        self.assertEqual(dd(), Decimal('14.839'))

    def test_format_decimal_from_string(self):
        dd = PtnDecimal('14.839')
        self.assertEqual(dd(), Decimal('14.839'))

    def test_format_decimal_none(self):
        dd = PtnDecimal(None)
        self.assertIsNone(dd())
        
    def test_format_decimal_wrong(self):
        self.assertRaises(ValueError, PtnDecimal, "ABC")

    def test_format_decimal_from_float_sized(self):
        dd = PtnSizedDecimal(2)
        self.assertEqual(dd(14.839)(), Decimal('14.84'))

    def test_format_decimal_from_decimal_sized(self):
        dd = PtnSizedDecimal(2)
        self.assertEqual(dd(Decimal('14.839'))(), Decimal('14.84'))

    def test_format_decimal_from_string_sized(self):
        dd = PtnSizedDecimal(2)
        self.assertEqual(dd('14.839')(), Decimal('14.84'))

    def test_format_decimal_none_sized(self):
        dd = PtnSizedDecimal(2)
        self.assertIsNone(dd(None)())
        
    def test_format_decimal_wrong_sized(self):
        dd = PtnSizedDecimal(2)
        self.assertRaises(ValueError, dd, "ABC")

    def test_format_string_from_string(self):
        s = PtnString("Абвгд")
        self.assertEqual(s(), "Абвгд")

    def test_format_string_from_unicode(self):
        s = PtnString(u"Абвгд")
        self.assertEqual(s(), "Абвгд")

    def test_format_string_empty(self):
        s = PtnString(None)
        self.assertIsNone(s())

    def test_format_string_from_string_sized(self):
        s = PtnSizedString(3)
        s2 = s("Абвгд")()
        self.assertEqual(s2, "Абв")

    def test_format_string_from_unicode_sized(self):
        s = PtnSizedString(3)
        self.assertEqual(s(u"Абвгд")(), "Абв")

    def test_format_string_sized_empty(self):
        s = PtnSizedString(3)
        self.assertIsNone(s(None)())

    def test_format_unicode_from_string(self):
        u = PtnUnicode("Абвгд")
        self.assertEqual(u(), u"Абвгд")

    def test_format_unicode_from_unicode(self):
        u = PtnUnicode(u"Абвгд")
        self.assertEqual(u(), u"Абвгд")

    def test_format_unicode_empty(self):
        u = PtnUnicode(None)
        self.assertIsNone(u())

    def test_format_unicode_from_string_sized(self):
        u = PtnSizedUnicode(3)
        self.assertEqual(u("Абвгд")(), u"Абв")

    def test_format_unicode_from_unicode_sized(self):
        u = PtnSizedUnicode(3)
        self.assertEqual(u(u"Абвгд")(), u"Абв")

    def test_format_unicode_sized_empty(self):
        u = PtnSizedUnicode(3)
        self.assertIsNone(u(None)())

    def test_format_date_from_string(self):
        d = PtnDate("04.08.2016")
        self.assertEqual(d(), datetime.date(2016, 8, 4))

    def test_format_date_from_datetime(self):
        d = PtnDate(datetime.date(2016, 8, 4))
        self.assertEqual(d(), datetime.date(2016, 8, 4))

    def test_format_date_from_date(self):
        d = PtnDate(time.localtime())
        self.assertEqual(d(), datetime.date.today())
    
    def test_format_date_none(self):
        d = PtnDate(None)
        self.assertIsNone(d())
    
    def test_format_wrong_date(self):
        self.assertRaises(ValueError, PtnDate, "Abcde")
    
    def test_format_time_from_string(self):
        t = PtnTime("22:14:08")
        self.assertEqual(t(), datetime.time(22, 14, 8))

    def test_format_time_from_time(self):
        t = PtnTime(datetime.time(22, 14, 8))
        self.assertEqual(t(), datetime.time(22, 14, 8))

    def test_format_time_from_timetuple(self):
        ttp = time.localtime()
        t = PtnTime(ttp)
        self.assertEqual(t(), datetime.time(ttp[3], ttp[4], ttp[5]))

    def test_format_wrong_time(self):
        self.assertRaises(ValueError, PtnTime, "Abcde")
    
    def test_format_time_none(self):
        t = PtnTime(None)
        self.assertIsNone(t())
    
    def test_format_datetime_from_string(self):
        dt = PtnDateTime("13.09.1978 22:30")
        self.assertEqual(dt(), datetime.datetime(1978, 9, 13, 22, 30, 00))

    def test_format_datetime_from_datetime(self):
        dt = PtnDateTime(datetime.datetime(1978, 9, 13, 22, 30, 00))
        self.assertEqual(dt(), datetime.datetime(1978, 9, 13, 22, 30, 00))

    def test_format_datetime_from_timetuple(self):
        tt = time.localtime()
        dt = PtnDateTime(tt)
        self.assertEqual(dt(), datetime.datetime(tt[0], tt[1], tt[2], tt[3], tt[4], tt[5]))

    def test_format_datetime_wrong(self):
        self.assertRaises(ValueError, PtnDateTime, "7654321")
    
    def test_format_datetime_null(self):
        dt = PtnDateTime(None)
        self.assertIsNone(dt())
    
    def test_format_interval_from_string(self):
        i = PtnInterval("1 day")
        self.assertEqual(i(), datetime.timedelta(days=1))
    
    def test_format_interval_wrong(self):
        self.assertRaises(ValueError, PtnInterval, "Dddddddd")
    
    def test_format_interval_null(self):
        i = PtnInterval(None)
        self.assertIsNone(i())

    def test_format_json_from_string(self):
        js = PtnJSON('{"Foo": "bar"}')
        self.assertEqual(js(), {"Foo": "bar"})
    
    def test_format_json_null(self):
        js = PtnJSON(None)
        self.assertIsNone(js())
    
    def test_format_json_wrong(self):
        self.assertRaises(ValueError, PtnJSON, "Not JSON")

    def test_format_guid_from_string(self):
        uid = uuid.uuid4()
        guid = PtnGUID("{0}".format(uid))
        self.assertEqual(guid(), uid)

    def test_format_guid_null(self):
        uid = PtnGUID(None)
        self.assertIsNone(uid())

    def test_format_guid_wrong(self):
        self.assertRaises(ValueError, PtnGUID, "Not UUID")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPgTranslators)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
