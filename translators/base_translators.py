# -*- coding: utf-8 -*-
""" Shoe2
    Анти-ORM пакет для работы с базами данных PostgreSQL
    Классы преобразования данных
    Базовые классы преобразования данных для построения SQL запросов
    и форматировании полученных результатов
"""
import re

SHARED_CLIENT = None
TEMPLATE = re.compile("""[\\{\\}'"]+""")


class PgTranslator(object):
    """ Базовый класс трансформации переменных для построения SQL запросов
        Суть работы класса сводится к форматированию
        строкового шаблона pg_pattern по заданным правилам
    """
    pg_pattern = "{0}"

    def _translate(self, value):
        """ Интерпритация переданного значения """
        if self.value != value:
            self._set_value(value)
        return self.__class__.pg_pattern.format(self.value)

    def _validate(self, _):
        """ Предварительная проверка значения.
            Метод реализуется в дочерних классах
        """
        pass

    def _set_value(self, value):
        self.__value = 'NULL' if self.is_null(value) else value

    @property
    def value(self):
        return self.__value

    @staticmethod
    def is_null(value):
        return (value is None) or (value == 'NULL')

    def __init__(self, value):
        try:
            self._validate(value)
        except Exception as err:
            raise ValueError(err.message)
        self._set_value(value)

    def __str__(self):
        return self._translate(self.value)

    def __unicode__(self):
        return u"{0}".format(self._translate(self.value))

    def __repr__(self):
        return self._translate(self.value)


class PgSizedTranslator(PgTranslator):
    """ Класс трансформации переменных
        с возможностью ограничения длины значения
    """

    def _set_size(self, value):
        self.__size = value

    def __init__(self, value):
        val = None
        self._set_size(-1)
        if isinstance(value, int):
            self._set_size(value)
        else:
            val = value
        super(PgSizedTranslator, self).__init__(val)

    @property
    def size(self):
        return self.__size

    def _apply_size(self, value):
        if self.is_null(value) or self.size < 0:
            return value
        return value[:self.size]

    def _translate(self, value):
        if self.value != value:
            self._set_value(value)
        return self.__class__.pg_pattern.format(self._apply_size(self.value))

    def __call__(self, value):
        self._validate(value)
        self._set_value(value)
        return self


class PgArray(PgTranslator):
    """ Класс трансформации переменных в массив """
    pg_pattern = "ARRAY[{0}]"

    def __init__(self, template):
        self.__tail = template.pg_pattern
        PgTranslator.__init__(self, template)

    def _translate(self, values):
        value = self.__class__.pg_pattern.format(self.value)
        return self.__tail.format(value) + '[]'

    def __call__(self, values):
        pattern = self.value
        if isinstance(values, (tuple, list)):
            if values:
                self._set_value(",".join(["%s" % pattern(item)
                                          for item in values]))
            else:
                self._set_value(pattern(None))
        else:
            self._set_value(pattern(None))
        return self


class PtnTranslator(object):
    """ Базовый класс трансформации переменных
        для форматирования полученных результатов.
        Форматирование каждого элемента из кортежа данных
        происходит одним из потомков класса.
        И базовый класс и наследники являются функторами:
        форматирование происходит в момент вызова объекта
    """
    def __init__(self, value):
        self.__value = None
        self.value = value

    def _set_value(self, val):
        if isinstance(val, (str, unicode)):
            val = self._translate(val)
        return val

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        val = self._set_value(val)
        try:
            self._validate(val)
        except Exception as err:
            raise ValueError(err.message)
        self.__value = val

    def _translate(self, value):
        try:
            return eval(value)
        except:
            return value

    def cast(self, value):
        return value

    def _validate(self, _):
        pass

    def __call__(self):
        return None if self.value is None else self.cast(self.value)


class PtnSized(PtnTranslator):
    """ Класс трансформации переменных с возможностью
        ограничения длины (округления) значения.
        Выполнен в виде метакласса для классов, обладающих свойством
        размерности (точности)
    """
    def cast(self, value):
        return self._apply_size(value)

    def _apply_size(self, value):
        if (value is None) or (self.size < 0):
            return value
        return value[:self.size]


class PtnArray(object):
    """ Класс преобразования массивов PostgreSQL в списки Python """
    def __init__(self, template):
        self.__template = template

    def __call__(self, value):
        if not value:
            return []

        if isinstance(value, (list, tuple)):
            return [self.__template(item)() for item in value]

        if isinstance(value, (str, unicode)):
            if value.startswith('{'):
                value = '[' + value[1:]
            if value.endswith('}'):
                value = value[:-1] + ']'
            lst = eval(value)
            return [self.__template(item)() for item in lst]

        return [self.__template(value)(), ]
