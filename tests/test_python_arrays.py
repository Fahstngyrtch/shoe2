# -*- coding: utf-8 -*-
import os
import sys
import unittest
from decimal import Decimal
import uuid
import datetime

from translators import PtnBool, PtnInt2, PtnInt4, PtnInt8, PtnDate, PtnTime
from translators import PtnArray, PtnDateTime, PtnInterval, PtnJSON, PtnGUID
from translators import PtnFloat, PtnSizedFloat, PtnDecimal, PtnSizedDecimal
from translators import PtnString, PtnSizedString, PtnUnicode, PtnSizedUnicode

BASEDIR = os.path.dirname(os.path.abspath(__file__)) + "{0}..{0}".format(os.sep)
sys.path.append(BASEDIR)


class TestPgTranslators(unittest.TestCase):
    def test_array_of_bool(self):
        b = PtnArray(PtnBool)("{'t','f','t'}")
        self.assertEqual(b, [True, False, True])

    def test_array_of_bool_none(self):
        b = PtnArray(PtnBool)(None)
        self.assertEqual(b, [])

    def test_array_of_int2(self):
        i2 = PtnArray(PtnInt2)("{14,15,16}")
        self.assertEqual(i2, [14, 15, 16])

    def test_array_of_int2_none(self):
        i2 = PtnArray(PtnInt2)(None)
        self.assertEqual(i2, [])

    def test_array_of_int4(self):
        i4 = PtnArray(PtnInt4)("{180000,42,70}")
        self.assertEqual(i4, [180000, 42, 70])

    def test_array_of_int4_none(self):
        i4 = PtnArray(PtnInt4)(None)
        self.assertEqual(i4, [])

    def test_array_of_int8(self):
        i8 = PtnArray(PtnInt8)("{400000000000}")
        self.assertEqual(i8, [400000000000, ])

    def test_array_of_int8_none(self):
        i8 = PtnArray(PtnInt8)(None)
        self.assertEqual(i8, [])

    def test_array_of_double_to_float(self):
        fd = PtnArray(PtnFloat)("{14.839, 3.142}")
        self.assertEqual(fd, [14.839, 3.142])

    def test_array_of_double_to_decimal(self):
        fd = PtnArray(PtnDecimal)("{14.839,3.142}")
        self.assertEqual(fd, [Decimal('14.839'), Decimal('3.142')])

    def test_array_of_float_double_none(self):
        fd = PtnArray(PtnFloat)(None)
        self.assertEqual(fd, [])

    def test_array_of_float_decimal_none(self):
        fd = PtnArray(PtnDecimal)(None)
        self.assertEqual(fd, [])

    def test_array_of_double_to_float_sized(self):
        fd = PtnArray(PtnSizedFloat(2))("{14.839,3.142}")
        self.assertEqual(fd, [14.84, 3.14])

    def test_array_of_double_to_decimal_sized(self):
        fd = PtnArray(PtnSizedDecimal(2))("{14.839,3.142}")
        self.assertEqual(fd, [Decimal("14.84"), Decimal("3.14")])

    def test_array_of_float_double_none_sized(self):
        fd = PtnArray(PtnSizedFloat(2))(None)
        self.assertEqual(fd, [])

    def test_array_of_float_decimal_none_sized(self):
        fd = PtnArray(PtnSizedDecimal(2))(None)
        self.assertEqual(fd, [])

    def test_array_of_string(self):
        s = PtnArray(PtnString)("{'Абвгд','Клмно'}")
        self.assertEqual(s, ["Абвгд", "Клмно"])

    def test_array_of_string_from_unicode(self):
        s = PtnArray(PtnString)(u"{'Абвгд','Клмно'}")
        self.assertEqual(s, ["Абвгд", "Клмно"])

    def test_array_of_string_empty(self):
        s = PtnArray(PtnString)(None)
        self.assertEqual(s, [])

    def test_array_of_string_from_string_sized(self):
        s = PtnArray(PtnSizedString(3))
        self.assertEqual(s("{'Абвгд','Клмно'}"), ["Абв", "Клм"])

    def test_array_of_string_from_unicode_sized(self):
        s = PtnArray(PtnSizedString(3))
        self.assertEqual(s(u"{'Абвгд','Клмно'}"), ["Абв", "Клм"])

    def test_array_of_string_sized_empty(self):
        s = PtnArray(PtnSizedString(3))(None)
        self.assertEqual(s, [])

    def test_array_of_unicode_from_string(self):
        u = PtnArray(PtnUnicode)("{'Абвгд','Клмно'}")
        self.assertEqual(u, [u"Абвгд", u"Клмно"])

    def test_array_of_unicode_from_unicode(self):
        u = PtnArray(PtnUnicode)(u"{'Абвгд','Клмно'}")
        self.assertEqual(u, [u"Абвгд", u"Клмно"])

    def test_array_of_unicode_empty(self):
        u = PtnArray(PtnUnicode)(None)
        self.assertEqual(u, [])

    def test_array_of_unicode_from_string_sized(self):
        u = PtnArray(PtnSizedUnicode(3))
        self.assertEqual(u("{'Абвгд','Клмно'}"), [u"Абв", u"Клм"])

    def test_array_of_unicode_from_unicode_sized(self):
        u = PtnArray(PtnSizedUnicode(3))
        self.assertEqual(u(u"{'Абвгд','Клмно'}"), [u"Абв", u"Клм"])

    def test_array_of_unicode_sized_empty(self):
        u = PtnArray(PtnSizedUnicode(3))(None)
        self.assertEqual(u, [])

    def test_array_of_date_from_string(self):
        d = PtnArray(PtnDate)("{'04.08.2016','04.08.2017'}")
        self.assertEqual(d, [datetime.date(2016, 8, 4), datetime.date(2017, 8, 4)])

    def test_array_of_date_none(self):
        d = PtnArray(PtnDate)(None)
        self.assertEqual(d, [])

    def test_array_of_time_from_string(self):
        t = PtnArray(PtnTime)("{'22:14:08','23:14:56'}")
        self.assertEqual(t, [datetime.time(22, 14, 8), datetime.time(23, 14, 56)])

    def test_array_of_time_none(self):
        t = PtnArray(PtnTime)(None)
        self.assertEqual(t, [])
    
    def test_array_of_datetime_from_string(self):
        dt = PtnArray(PtnDateTime)("{'13.09.1978 22:30','24.04.1987 08:00'}")
        self.assertEqual(dt, [datetime.datetime(1978, 9, 13, 22, 30, 00), datetime.datetime(1987, 4, 24, 8, 0, 0)])

    def test_array_of_datetime_none(self):
        dt = PtnArray(PtnDateTime)(None)
        self.assertEqual(dt, [])
    
    def test_array_of_interval_from_string(self):
        i = PtnArray(PtnInterval)("{'1 day','1 hour'}")
        self.assertEqual(i, [datetime.timedelta(days=1), datetime.timedelta(hours=1)])

    def test_array_of_interval_none(self):
        i = PtnArray(PtnInterval)(None)
        self.assertEqual(i, [])
    
    def test_array_of_json_from_string(self):
        js = PtnArray(PtnJSON)("""{'{"Foo": "bar"}','{"Foo": "Baz"}'}""")
        self.assertEqual(js, [{"Foo": "bar"}, {"Foo": "Baz"}])
    
    def test_array_of_json_none(self):
        js = PtnArray(PtnJSON)(None)
        self.assertEqual(js, [])

    def test_array_of_guid_from_string(self):
        uid = uuid.uuid4()
        uid2 = uuid.uuid4()
        guid = PtnArray(PtnGUID)("{'%s','%s'}" % (uid, uid2))
        self.assertEqual(guid, [uid, uid2])

    def test_array_of_guid_none(self):
        uid = PtnArray(PtnGUID)(None)
        self.assertEqual(uid, [])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPgTranslators)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
