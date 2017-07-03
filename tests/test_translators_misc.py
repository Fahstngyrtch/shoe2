import datetime
import os
import sys
import time
import unittest

BASEDIR = os.path.dirname(os.path.abspath(__file__)) + "{0}..{0}".format(os.sep)
sys.path.append(BASEDIR)

from translators.misc import make_date, make_time, make_datetime, make_interval


class TestMisc(unittest.TestCase):
    # testing make_date

    def test_make_date_from_none_for_postgres(self):
        res = make_date(None)
        self.assertEqual(res, 'NULL')

    def test_make_date_from_none_for_python(self):
        res = make_date(None, False)
        self.assertIsNone(res)

    def test_make_date_from_string_for_postgres(self):
        res = make_date("05.05.17")
        self.assertEqual(res, "05.05.2017")

    def test_make_date_from_string_for_python(self):
        res = make_date("05.05.17", False)
        self.assertEqual(res, datetime.date(2017, 5, 5))

    def test_make_date_from_wrong_string_for_postgres(self):
        self.assertRaises(ValueError, make_date, "abc")

    def test_make_date_from_wrong_string_for_python(self):
        self.assertRaises(ValueError, make_date, "abc", False)

    def test_make_date_from_empty_string_for_postgres(self):
        res = make_date('')
        self.assertEqual(res, 'NULL')

    def test_make_date_from_empty_string_for_python(self):
        res = make_date('', False)
        self.assertIsNone(res)

    def test_make_date_from_int_for_postgres(self):
        self.assertRaises(TypeError, make_date, 42)

    def test_make_date_from_int_for_python(self):
        self.assertRaises(TypeError, make_date, 42, False)

    def test_make_date_from_timetuple_for_postgres(self):
        now = time.localtime()
        res = make_date(now)
        self.assertEqual(res, time.strftime("%d.%m.%Y", now))

    def test_make_date_from_timetuple_for_python(self):
        now = time.localtime()
        etalon = datetime.date.fromtimestamp(time.mktime(now))
        res = make_date(now, False)
        self.assertEqual(res, etalon)

    def test_make_date_from_date_for_postgres(self):
        now = datetime.date.today()
        res = make_date(now)
        self.assertEqual(res, now.strftime("%d.%m.%Y"))

    def test_make_date_from_date_for_python(self):
        now = datetime.date.today()
        res = make_date(now, False)
        self.assertEqual(res, now)

# testing make_time

    def test_make_time_from_none_for_postgres(self):
        res = make_time(None)
        self.assertEqual(res, 'NULL')

    def test_make_time_from_none_for_python(self):
        res = make_time(None, False)
        self.assertIsNone(res)

    def test_make_time_from_string_for_postgres(self):
        res = make_time("12:00")
        self.assertEqual(res, "12:00")

    def test_make_time_from_string_for_python(self):
        res = make_time("12:00", False)
        self.assertEqual(res, datetime.time(12))

    def test_make_time_from_wrong_string_for_postgres(self):
        self.assertRaises(ValueError, make_time, "46:")

    def test_make_time_from_wrong_string_for_python(self):
        self.assertRaises(ValueError, make_time, "46:", False)

    def test_make_time_from_empty_string_for_postgres(self):
        res = make_time('')
        self.assertEqual(res, 'NULL')

    def test_make_time_from_empty_string_for_python(self):
        res = make_time('', False)
        self.assertIsNone(res)

    def test_make_time_from_int_for_postgres(self):
        self.assertRaises(TypeError, make_time, 404)

    def test_make_time_from_int_for_python(self):
        self.assertRaises(TypeError, make_time, 404, False)

    def test_make_time_from_timetuple_for_postgres(self):
        tt = time.localtime()
        res = make_time(tt)
        self.assertEqual(res, time.strftime("%H:%M:%S", tt))

    def test_make_time_from_timetuple_for_python(self):
        tt = time.localtime()
        etalon = datetime.time(tt[3], tt[4], tt[5])
        res = make_time(tt, False)
        self.assertEqual(res, etalon)

    def test_make_time_from_time_for_postgres(self):
        tm = datetime.time(13, 2, 4)
        res = make_time(tm)
        self.assertEqual(res, tm.strftime("%H:%M:%S"))

    def test_make_time_from_time_for_python(self):
        tm = datetime.time(13, 2, 4)
        res = make_time(tm, False)
        self.assertEqual(res, tm)

# testing make_datetime
    
    def test_make_datetime_from_none_for_postgres(self):
        res = make_datetime(None)
        self.assertEqual(res, 'NULL')

    def test_make_datetime_from_none_for_python(self):
        res = make_datetime(None, False)
        self.assertIsNone(res)

    def test_make_datetime_from_string_for_postgres(self):
        res = make_datetime("17.03.2015 18:00:08")
        self.assertEqual(res, "17.03.2015 18:00:08")

    def test_make_datetime_from_string_for_python(self):
        res = make_datetime("17.03.2015 18:00:08", False)
        etalon = datetime.datetime(2015, 3, 17, 18, 0, 8)
        self.assertEqual(res, etalon)

    def test_make_datetime_from_wrong_string_for_postgres(self):
        self.assertRaises(ValueError, make_datetime, "41.02.2033#AA:13")

    def test_make_datetime_from_wrong_string_for_python(self):
        self.assertRaises(ValueError, make_datetime, "41.02.2033#AA:13", False)

    def test_make_datetime_from_empty_string_for_postgres(self):
        res = make_datetime('')
        self.assertEqual(res, 'NULL')

    def test_make_datetime_from_empty_string_for_python(self):
        res = make_datetime('', False)
        self.assertIsNone(res)

    def test_make_datetime_from_int_for_postgres(self):
        self.assertRaises(TypeError, make_datetime, 4)

    def test_make_datetime_from_int_for_python(self):
        self.assertRaises(TypeError, make_datetime, 4, False)

    def test_make_datetime_from_timetuple_for_postgres(self):
        now = time.localtime()
        res = make_datetime(now)
        self.assertEqual(res, time.strftime("%d.%m.%Y %H:%M:%S", now))

    def test_make_datetime_from_timetuple_for_python(self):
        now = time.localtime()
        etalon = datetime.datetime(*now[:6])
        res = make_datetime(now, False)
        self.assertEqual(res, etalon)

    def test_make_datetime_from_datetime_for_postgres(self):
        now = datetime.datetime.now()
        res = make_datetime(now)
        self.assertEqual(res, now.strftime("%d.%m.%Y %H:%M:%S"))

    def test_make_datetime_from_datetime_for_python(self):
        now = datetime.datetime.now()
        res = make_datetime(now, False)
        self.assertEqual(res, now)

# testing make_interval

    def test_make_interval_from_none_for_postgres(self):
        res = make_interval(None)
        self.assertEqual(res, 'NULL')

    def test_make_interval_from_none_for_python(self):
        res = make_interval(None, False)
        self.assertIsNone(res)
    
    def test_make_interval_from_timedelta_for_postgres(self):
        td = datetime.timedelta(hours=1)
        res = make_interval(td)
        self.assertEqual(res, '3600 second')

    def test_make_interval_from_timedelta_for_python(self):
        td = datetime.timedelta(hours=1)
        res = make_interval(td, False)
        self.assertEqual(res, td)

    def test_make_interval_from_int_for_postgres(self):
        res = make_interval(1)
        self.assertEqual(res, '3600 second')

    def test_make_interval_from_int_for_python(self):
        res = make_interval(1, False)
        etalon = datetime.timedelta(hours=1)
        self.assertEqual(res, etalon)

    def test_make_interval_from_wrong_string_for_postgres(self):
        self.assertRaises(ValueError, make_interval, "ABC123second")

    def test_make_interval_from_wrong_string_for_python(self):
        self.assertRaises(ValueError, make_interval, "ABC123", False)

    def test_make_interval_from_empty_string_for_postgres(self):
        res = make_interval('')
        self.assertEqual(res, 'NULL')

    def test_make_interval_from_empty_string_for_python(self):
        res = make_interval('', False)
        self.assertIsNone(res)

    def test_make_interval_from_string_for_postgtres(self):
        res = make_interval("00:02:00")
        self.assertEqual(res, "120 second")

    def test_make_interval_from_string_for_python(self):
        res = make_interval("00:02:00", False)
        self.assertEqual(res, datetime.timedelta(minutes=2))

    def test_make_interval_from_week_for_postgres(self):
        res = make_interval("1 week")
        self.assertEqual(res, "604800 second")

    def test_make_interval_from_week_for_python(self):
        res = make_interval("1 week", False)
        self.assertEqual(res, datetime.timedelta(weeks=1))

    def test_make_interval_from_day_for_postgres(self):
        res = make_interval("1 day")
        self.assertEqual(res, "86400 second")

    def test_make_interval_from_day_for_python(self):
        res = make_interval("1 day", False)
        self.assertEqual(res, datetime.timedelta(days=1))

    def test_make_interval_from_hour_for_postgres(self):
        res = make_interval("1 hour")
        self.assertEqual(res, "3600 second")

    def test_make_interval_from_hour_for_python(self):
        res = make_interval("1 hour", False)
        self.assertEqual(res, datetime.timedelta(hours=1))

    def test_make_interval_from_minute_for_postgres(self):
        res = make_interval("1 minute")
        self.assertEqual(res, "60 second")

    def test_make_interval_from_minute_for_python(self):
        res = make_interval("1 minute", False)
        self.assertEqual(res, datetime.timedelta(minutes=1))

    def test_make_interval_from_second_for_postgres(self):
        res = make_interval("10 seconds")
        self.assertEqual(res, "10 second")

    def test_make_interval_from_second_for_python(self):
        res = make_interval("10 seconds", False)
        self.assertEqual(res, datetime.timedelta(seconds=10))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMisc)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
