# -*- coding: utf-8 -*-
""" Shoe2
    Анти-ORM пакет для работы с базами данных PostgreSQL
    Классы преобразования данных
    Профильные классы для форматирования результатов запроса
"""
from decimal import Decimal
import uuid
import json

from misc import make_date, make_time, make_datetime, make_interval
from base_translators import PtnTranslator


class AsBool(PtnTranslator):
    """ Преобразование булевых значений """
    pattern = "TRUE1"

    def cast(self, value):
        if value is None:
            return value
        return str(value).upper() in self.pattern


class AsInt2(PtnTranslator):
    """ Короткое целое """
    def _validate(self, value):
        if value is not None:
            return int(value)

    def cast(self, value):
        return int(value) if value is not None else None


class AsInt4(AsInt2):
    """ Целое """


class AsInt8(AsInt2):
    """ Длинное целое """
    def _validate(self, value):
        if value is not None:
            return long(value)

    def cast(self, value):
        return long(value) if value is not None else None


class AsFloat(PtnTranslator):
    """ Преобразование во float """
    def _set_value(self, val):
        val = super(AsFloat, self)._set_value(val)
        if val is not None:
            if isinstance(val, Decimal):
                val = float(str(val))
            else:
                self._validate(val)
                val = float(val)
        return val

    def _validate(self, value):
        if value is not None:
            try:
                return float(value)
            except Exception as err:
                raise ValueError(err.message)


class AsDecimal(PtnTranslator):
    """ Преобразование в Decimal """
    def _set_value(self, val):
        val = super(AsDecimal, self)._set_value(val)
        if val is not None:
            if not isinstance(val, Decimal):
                self._validate(val)
                val = Decimal(str(val))
        return val

    def _validate(self, value):
        if value is not None:
            try:
                return Decimal(value)
            except Exception as err:
                raise ValueError(err.message)


class AsDate(PtnTranslator):
    """ Преобразование в datetime.date """
    def _validate(self, value):
        return make_date(value)

    def cast(self, value):
        if value is None:
            return None
        return make_date(value, False)


class AsTime(PtnTranslator):
    """ Преобразование в datetime.time """
    def _validate(self, value):
        return make_time(value)

    def cast(self, value):
        if value is None:
            return None
        return make_time(value, False)


class AsDateTime(PtnTranslator):
    """ Преобразование в datetime.datetime """
    def _validate(self, value):
        return make_datetime(value)

    def cast(self, value):
        if value is None:
            return None
        return make_datetime(value, False)


class AsInterval(PtnTranslator):
    """ Преобразование в datetime.interval """
    def _validate(self, value):
        return make_interval(value)

    def cast(self, value):
        if value is None:
            return None
        return make_interval(value, False)


class AsUnicode(PtnTranslator):
    """ Преобразование в юникод с возможностью ограничения по длине """
    def _translate(self, value):
        return value

    def _set_value(self, val):
        val = super(AsUnicode, self)._set_value(val)
        if val is not None:
            if isinstance(val, str):
                val = val.decode('utf-8')
            else:
                val = unicode(val)
        return val


class AsString(AsUnicode):
    """ Преобразование в строку с возможностью ограничения по длине """
    def _translate(self, value):
        return value

    def cast(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            return value
        if isinstance(value, unicode):
            return value.encode('utf-8')
        return str(value)


class AsGUID(PtnTranslator):
    """ Преобразование в uuid """
    def _validate(self, value):
        if value is not None:
            return uuid.UUID('{%s}' % value)

    def cast(self, value):
        if value is None:
            return None
        return uuid.UUID('{%s}' % value)


class AsJSON(PtnTranslator):
    """ Преобразование в словарь """
    def _translate(self, value):
        return value

    def _validate(self, value):
        if value is not None:
            if isinstance(value, dict):
                return value
            return json.loads(value, 'utf-8')

    def cast(self, value):
        if value is None:
            return None

        if isinstance(value, dict):
            return value

        return json.loads(value, 'utf-8')
