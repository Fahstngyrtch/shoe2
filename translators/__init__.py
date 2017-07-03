# -*- coding: utf-8 -*-
""" Shoe2
    Анти-ORM пакет для работы с базами данных PostgreSQL
    Классы преобразования данных
"""
from functools import wraps
from decimal import Decimal

from base_translators import PgArray, PtnArray, PtnSized
import pg_translators
import python_translators


PgBool = pg_translators.Bool
PgInt2 = pg_translators.Int2
PgInt4 = pg_translators.Int4
PgInt8 = pg_translators.Int8
PgFloatNumeric = pg_translators.FloatNumeric
PgFloatDouble = pg_translators.FloatDouble
PgDecimalNumeric = pg_translators.DecimalNumeric
PgDecimalDouble = pg_translators.DecimalDouble
PgDate = pg_translators.Date
PgTime = pg_translators.Time
PgDateTime = pg_translators.DateTime
PgInterval = pg_translators.Interval
PgSafeString = pg_translators.SafeString
PgString = pg_translators.String
PgText = pg_translators.Text
PgGUID = pg_translators.GUID
PgJSON = pg_translators.JSON

PtnBool = python_translators.AsBool
PtnInt2 = python_translators.AsInt2
PtnInt4 = python_translators.AsInt4
PtnInt8 = python_translators.AsInt8
PtnFloat = python_translators.AsFloat
PtnDecimal = python_translators.AsDecimal
PtnDate = python_translators.AsDate
PtnTime = python_translators.AsTime
PtnDateTime = python_translators.AsDateTime
PtnInterval = python_translators.AsInterval
PtnString = python_translators.AsString
PtnUnicode = python_translators.AsUnicode
PtnGUID = python_translators.AsGUID
PtnJSON = python_translators.AsJSON

# Обертки над классами, обладающими свойством размерности (точности)
# Ограничения размера (точности) задаются предварительно, чтобы к моменту
# инициализации объекта-транслятора уже была известна его размерность (точность)


def PtnSizedFloat(accuracy):
    """ Обертка над типа float
        :param accuracy: точность округления
        :returns: Переопределенный класс AsFloat, обладающий заданной точностью
    """
    class AsSizedFloat(PtnFloat, PtnSized):
        size = accuracy

        def _apply_size(self, value):
            if (value is None) or (self.size < 0):
                return value
            return round(value, self.size)
    return AsSizedFloat


def PtnSizedDecimal(accuracy):
    """ Обработка типа Decimal
        :param accuracy: точность округления
        :returns: Переопределенный класс AsDecimal,
                  обладающий заданной точностью
    """
    class AsSizedDecimal(PtnDecimal, PtnSized):
        size = accuracy

        def _apply_size(self, value):
            if (value is None) or (self.size < 0):
                return value
            return Decimal.quantize(value, Decimal("0." + "0" * self.size))
    return AsSizedDecimal


def PtnSizedString(length):
    """ Обработка типа str
        :param length: точность округления
        :returns: Переопределенный класс AsString, обладающий заданной длинной
    """
    class AsSizedString(PtnString, PtnSized):
        size = length

        def cast(self, value):
            return PtnString.cast(self, self._apply_size(value))
    return AsSizedString


def PtnSizedUnicode(length):
    """ Обработка типа unicode
        :param length: точность округления
        :returns: Переопределенный класс AsUnicode, обладающий заданной длинной
    """
    class AsSizedUnicode(PtnUnicode, PtnSized):
        size = length
    return AsSizedUnicode


def _translate(objects, args):
    """ Слияние списка объектов-преобразователей со списком аргументов
        :param objects: Кортеж классов-преобразователей (П1, П2, ...)
        :param args: Аргументы для преобразования (А1, А2, ...)
        :returns Список пар вида [(П1, А1), (П2, А2), ...]
    """
    args_map = zip(objects, args)
    try:
        return tuple([i(j) for i, j in args_map])
    except Exception as err:
        raise ValueError(err.message)


def append_list(lst1, lst2, default=None, cut=False):
    """ Выравнивание двух списков по длине путем дополнения
        короткого списка значениями по умолчанию
        :param lst1: список 1
        :param lst2: список 2
        :param default: заполнитель
        :param cut: уравнивание списков по длине путем отсечения
    """
    delta = len(lst1) - len(lst2)
    if delta == 0:
        return

    if delta < 0:
        if cut:
            lst2 = lst2[:len(lst1)]
        else:
            lst1 += [default, ] * abs(delta)
    else:
        if cut:
            lst1 = lst1[:len(lst2)]
        else:
            lst2 += [default, ] * abs(delta)


def _retranslate(pattern, result):
    """ Преобразование результата выборки
        предложенными классами трансформации
        :param pattern: шаблон строки под обработку данных. Шаблон повторяет
        структуру возвращаемого кортежа данных и соотносится с типом кортежа.
        Это может юыть словарь вида {'Имя_поля': Класс, ...}, список
        или класс для обработки атомарных результатов запроса
        :result: результат выполнения запроса. Может быть генератором, списком
        словарей или кортежей, одиночным словарем или кортежем,
        одиночным значением.
        :returns в зависимости от типа результата возвращает соответствующий
        набор преобразованных значений
    """
    if (result is None) or (pattern is None):
        return result

    def turn_generator():
        """ Преобразование генератора """
        for itm in result:
            yield worker(itm)

    def turn_dictionary(row):
        """ Преобразование словаря """
        if not isinstance(pattern, dict):
            raise TypeError(u"Шаблон должен быть задан в виде словаря")

        for key in row.keys():
            if key in pattern:
                if pattern[key] is not None:
                    row[key] = pattern[key](row[key])()
        return row

    def turn_tuple(row):
        """ Преобразование кортежа """
        if not isinstance(pattern, (tuple, list)):
            raise TypeError(u"Шаблон должен быть задан "
                            u"в виде списка или кортежа")

        row = list(row)
        append_list(pattern, row)
        for idx, itm in enumerate(row):
            if pattern[idx] is None:
                continue
            row[idx] = pattern[idx](itm)()
        return tuple(row)

    def turn_value(value):
        """ Преобразование атомарного типа """
        if isinstance(pattern, dict):
            cls = pattern.values()[0]
        elif isinstance(pattern, (list, tuple)):
            cls = pattern[0]
        else:
            cls = pattern

        if cls is None:
            return value

        return cls(value)()

    if isinstance(pattern, dict):
        worker = turn_dictionary
    elif isinstance(pattern, (tuple, list)):
        worker = turn_tuple
    else:
        worker = turn_value

    # обработка генераторов словарей и кортежей
    if hasattr(result, 'next'):
        return turn_generator()
    # обработка списков словарей и кортежей
    if isinstance(result, list):
        return [worker(item) for item in result]
    # обработка словаря или кортежа
    if isinstance(result, (dict, tuple)):
        return worker(result)
    # обработка атомарного значения
    return worker(result)


def translate(*translators):
    """ Преобразование входных параметров для формирования SQL запроса
        Реализация в виде декоратора
    """
    def maker(func):
        @wraps(func)
        def wrap_function(*args):
            args = _translate(translators, args)
            return func(*args)

        @wraps(func)
        def wrap_method(self, *args):
            args = _translate(translators, args)
            return func(self, *args)

        if ('self' in func.func_code.co_varnames) \
                or (hasattr(func, 'is_method')):
            return wrap_method
        return wrap_function
    return maker


def retranslate(pattern):
    """ Преобразование  данных, полученных запросов к базе
        Реализация в виде декоратора
        :param pattern: список классов трансформации
    """
    def maker(func):
        @wraps(func)
        def wrap_function(*args, **kwargs):
            kwargs['result'] = _retranslate(pattern, kwargs['result'])
            return func(*args, **kwargs)

        @wraps(func)
        def wrap_method(self, *args, **kwargs):
            kwargs['result'] = _retranslate(pattern, kwargs['result'])
            return func(self, *args, **kwargs)

        if('self' in func.func_code.co_varnames) \
                or (hasattr(func, 'is_method')):
            return wrap_method
        return wrap_function
    return maker
