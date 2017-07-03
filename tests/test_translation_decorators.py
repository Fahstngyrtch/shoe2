import datetime
import os
import sys
import time
import unittest

BASEDIR = os.path.dirname(os.path.abspath(__file__)) + "{0}..{0}".format(os.sep)
sys.path.append(BASEDIR)

from translators import translate, PgInt4, PgString


class TestDecorators(unittest.TestCase):
    # testing translation decorators

    def test_translation_decorators_for_function(self):
        @translate(PgInt4)
        def translate_integer(x):
            return "{0}".format(x)

        self.assertEqual(translate_integer(4), "4::int4")

    def test_translation_decorators_of_limited_objects_for_instances(self):
        class MyInstance(object):
            @translate(PgString(4))
            def do_it(self, value):
                return "{0}".format(value)

        self.assertEqual(MyInstance().do_it("Abcdefgh"), "'Abcd'::varchar")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDecorators)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
