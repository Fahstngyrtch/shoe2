# -*- coding: utf-8 -*-
""" Shoe2
    Анти-ORM пакет для работы с базами данных PostgreSQL
    Классы преобразования данных
    Профильные классы преобразования данных для построения SQL запросов
"""
from decimal import Decimal
import re
import uuid
import json

from base_translators import PgTranslator, PgSizedTranslator
from misc import make_date, make_time, make_datetime, make_interval

SAVE_TEMPLATE = re.compile("""[\\\\/;'"`$#]+""")
ARRAY_TEMPLATE = re.compile("[\\{|\\}]")


class Bool(PgTranslator):
    """ Преобразование булевых значений """
    pg_pattern = '{0}::boolean'
    pattern = "TRUE1"

    def _translate(self, value):
        if self.is_null(value):
            return 'NULL::boolean'
        return "{0}".format(str(value).upper() in self.pattern)


class Int2(PgTranslator):
    """ Преобразование малых целых чисел """
    pg_pattern = '{0}::int2'

    def _validate(self, value):
        if not self.is_null(value):
            try:
                int(value)
            except Exception as err:
                raise ValueError(err.message)

            if int(value) > 32767:
                raise ValueError(u"Малое целое должно быть меньше 32767")


class Int4(PgTranslator):
    """ Преобразование целых чисел """
    pg_pattern = '{0}::int4'

    def _validate(self, value):
        if not self.is_null(value):
            try:
                int(value)
            except Exception as err:
                raise ValueError(err.message)


class Int8(PgTranslator):
    """ Преобразование больших целых чисел """
    pg_pattern = '{0}::int8'

    def _validate(self, value):
        if not self.is_null(value):
            try:
                int(value)
            except Exception as err:
                raise ValueError(err.message)


class FloatNumeric(PgSizedTranslator):
    """ Преобразование float в numeric """
    pg_pattern = '{0}::numeric'

    def _apply_size(self, value):
        if self.is_null(value) or self.size < 0:
            return value
        return round(value, self.size)

    def _validate(self, value):
        if not self.is_null(value):
            try:
                float(value)
            except Exception as err:
                raise ValueError(err.message)


class DecimalNumeric(PgSizedTranslator):
    """ Преобразование Decimal в numeric """
    pg_pattern = '{0}::numeric'

    def _apply_size(self, value):
        if self.is_null(value) or self.size < 0:
            return value
        return Decimal.quantize(value, Decimal("0." + "0" * self.size))

    def _validate(self, value):
        if not self.is_null(value):
            if isinstance(value, float):
                value = str(value)
            try:
                Decimal(value)
            except Exception as err:
                raise ValueError(err.message)


class FloatDouble(FloatNumeric):
    """ Преобразование float в double """
    pg_pattern = '{0}::double'


class DecimalDouble(DecimalNumeric):
    """ Преобразование Decimal в double """
    pg_pattern = '{0}::double'


class Date(PgTranslator):
    """ Преобразование даты в тип date.
        Дата может быть представлена объектом типа datetime.date,
        временным кортежем или строкой
    """
    pg_pattern = "{0}::date"

    def _validate(self, value):
        try:
            make_date(value)
        except Exception as err:
            raise ValueError(err.message)

    def _translate(self, value):
        if self.is_null(value):
            date = 'NULL'
        else:
            date = "'{0}'".format(make_date(value))
        return self.pg_pattern.format(date)


class Time(PgTranslator):
    """ Преобразование времени в тип time.
        Время может быть представлено в виде объекта типа datetime.time,
        временного кортежа или строки
    """
    pg_pattern = "{0}::time"

    def _validate(self, value):
        try:
            make_time(value)
        except Exception as err:
            raise ValueError(err.message)

    def _translate(self, value):
        if self.is_null(value):
            time = 'NULL'
        else:
            time = "'{0}'".format(make_time(value))
        return self.pg_pattern.format(time)


class DateTime(PgTranslator):
    """ Преобразование даты и времени в timestamp.
        Значение может быть задано объектом типа datetime.datetime,
        временным кортежем или строкой
    """
    pg_pattern = "{0}::timestamp"

    def _validate(self, value):
        try:
            make_datetime(value)
        except Exception as err:
            raise ValueError(err.message)

    def _translate(self, value):
        if self.is_null(value):
            datetime = 'NULL'
        else:
            datetime = "'{0}'".format(make_datetime(value))
        return self.pg_pattern.format(datetime)


class Interval(PgTranslator):
    """ Преобразование временного интервала в тип interval
        Значение может быть задано объектом datetime.timedelta, числом,
        обозначающим количество часов,
        либо строкой с указанием часов, минут и секунд, разделенных символом ':'
    """
    pg_pattern = "{0}::interval"

    def _validate(self, value):
        try:
            make_interval(value)
        except Exception as err:
            raise ValueError(err.message)

    def _translate(self, value):
        if self.is_null(value):
            interval = 'NULL'
        else:
            interval = "'{0}'".format(make_interval(value))
        return self.pg_pattern.format(interval)


class String(PgSizedTranslator):
    """ Преобразование строки """
    pg_pattern = "{0}::varchar"

    def _set_value(self, value):
        val = None
        if not self.is_null(value):
            if isinstance(value, str):
                val = value.decode('utf-8')
            elif isinstance(value, unicode):
                val = value
            else:
                val = unicode(value, 'utf-8')
        super(String, self)._set_value(val)

    def _translate(self, value):
        if self.value != value:
            self._set_value(value)
        value = self._apply_size(self.value).encode('utf-8')
        if not self.is_null(value):
            value = "'{0}'".format(value)
        return self.pg_pattern.format(value)

    def _validate(self, value):
        if self.is_null(value):
            return
        if isinstance(value, (str, unicode)):
            return
        try:
            unicode(value, 'utf-8')
        except Exception as err:
            raise ValueError(err.message)


class SafeString(String):
    """ Преобразование строки с исключением специальных символов """
    def _set_value(self, value):
        if self.is_null(value):
            super(SafeString, self)._set_value(None)
        else:
            super(SafeString, self)._set_value(re.sub(SAVE_TEMPLATE, '', value))

    def _translate(self, value):
        if self.value != value:
            self._set_value(value)
        return super(SafeString, self)._translate(self.value)


class Text(PgTranslator):
    """ Преобразование обычной или юникод-строки в тип text """
    pg_pattern = "{0}::text"

    def _translate(self, value):
        if self.is_null(value):
            value = 'NULL'
        else:
            if isinstance(value, unicode):
                value = value.decode('utf-8')

        value = 'NULL' if self.is_null(value) else "'{0}'".format(value)
        return self.pg_pattern.format(value)


class GUID(PgTranslator):
    """ Преобразование UUID объекта в GUID """
    pg_pattern = "{0}::guid"

    def __init__(self, value):
        if not self.is_null(value):
            try:
                uuid.UUID('{%s}' % value)
            except Exception as err:
                raise ValueError(err.message)
        super(GUID, self).__init__(value)

    def _translate(self, value):
        if self.is_null(value):
            value = 'NULL'
        else:
            if isinstance(value, unicode):
                value = value.decode('utf-8')

        value = 'NULL' if self.is_null(value) else "'{0}'".format(value)
        return self.pg_pattern.format(value)


class JSON(PgTranslator):
    """ Преобразование словаря в тип jsonb """
    pg_pattern = "{0}::jsonb"

    def __init__(self, value):
        if not self.is_null(value):
            if not isinstance(value, dict):
                try:
                    value = json.loads(value)
                except Exception as err:
                    raise ValueError(err)
        super(JSON, self).__init__(value)

    def _translate(self, value):
        if self.is_null(value):
            value = 'NULL'
        else:
            value = "'{0}'".format(json.dumps(value))
        return self.pg_pattern.format(value)
