# -*- coding: utf-8 -*-
""" Shoe2
    Анти-ORM пакет для работы с базами данных PostgreSQL
    Управление структурой возвращаемых данных
"""
from functools import wraps

from query_models import BaseQuery, DynamicBaseQuery, StaticBaseQuery
from custom_errors import DataError


class CustomManager(object):
    """ Базовый класс представления результатов выборки """
    @staticmethod
    def as_generator_of_dictionaries(result):
        """ Результат выборки в виде генератора словарей
        :param result: результат выборки
        :return: генератор
        """
        return BaseQuery.as_dict(result)

    @staticmethod
    def as_dictionaries(result, look4empty=False):
        """ Результат выборки в виде списка словарей
        :param result: результат выборки
        :param look4empty: проверка на непустоту результата
        :return: список словарей
        """
        if not result:
            if look4empty:
                raise DataError(code=1).describe(u"Нет данных")
        return [item for item in BaseQuery.as_dict(result)]

    @staticmethod
    def as_dictionary(result, look4empty=False):
        """ Результат выборки в виде одного словаря (первая запись)
            :param result: результат выборки
            :param look4empty: проверка на непустоту результата
            :return: словарь
        """
        data = BaseQuery.as_dict(result).next()
        if look4empty:
            if not data:
                raise DataError(code=1).describe(u"Нет данных")
        return data

    @staticmethod
    def as_generator_of_tuples(result):
        """ Результат выборки в виде генератора кортежей
            :param result: результат выборки
            :return: генератор
        """
        return BaseQuery.as_tuple_(result)

    @staticmethod
    def as_tuples(result, look4empty=False):
        """ Результат выборки в виде списка кортежей
            :param result: результат выборки
            :param look4empty: проверка на непустоту результата
            :return: список кортежей
        """
        if not result:
            if look4empty:
                raise DataError(code=1).describe(u"Нет данных")
        return [item for item in BaseQuery.as_tuple_(result)]

    @staticmethod
    def as_tuple(result, look4empty=False):
        """ Результат выборки в виде кортежа (первая запись)
            :param result: результат выборки
            :param look4empty: проверка на непустоту результата
            :return: кортеж
        """
        data = BaseQuery.as_tuple_(result).next()
        if look4empty:
            if not data:
                raise DataError(code=1).describe(u"Нет данных")
        return data

    @staticmethod
    def as_value(result, look4empty=False):
        """ Результат выборки в виде атомарного значения
            (первая колонка первой строки)
            :param result: результат выборки
            :param look4empty: проверка на непустоту результата
            :return: атомарное значение
        """
        data = BaseQuery.as_tuple_(result).next()
        if not data:
            if look4empty:
                raise DataError(code=1).describe(u"Нет данных")
        else:
            data = data[0]
        return data


class StaticDataManager(StaticBaseQuery):
    """ Модель статических запросов, совмещенная с менеджером обработки данных
        Методы, имеющие в названии префикс as_, используются напрямую
        Соответствующие им методы без префикса используются как декораторы
    """
    def __init__(self, connection):
        """ Конструктор класса
            :param connection: открытое подключение к базе данных
        """
        super(StaticBaseQuery, self).__init__(connection)

    def _middleware(self, is_method, query, *args):
        """ Прослойка для определения типа вызываемого объекта
            (метод или функция)
        """
        def wrap_function():
            return self.make_query(query, *args)

        def wrap_method():
            return self.make_query(query, *args[1:])

        return wrap_method() if is_method else wrap_function()

    def as_generator_of_dictionaries(self, query, *args, **kwargs):
        """ Результат выборки в виде генератора словарей
            :param query: текст SQL запроса
            :param args: переменные, подставляемые в текст запроса
            :param kwargs: служебный словарь для сохранения результатов выборки
        """
        return CustomManager.as_generator_of_dictionaries(
            self.make_query(query, *args, **kwargs))

    def generator_of_dictionaries(self, query):
        """ Результат выборки в виде генератора словарей
            :param query: текст SQL запроса (параметр декоратора)
        """
        def maker(function):
            is_instance = 'self' in function.func_code.co_varnames

            @wraps(function)
            def wrapper(*args, **kwargs):
                result = CustomManager.as_generator_of_dictionaries(
                    self._middleware(is_instance, query, *args))
                kwargs['result'] = result
                return function(*args, **kwargs)

            if is_instance:
                setattr(wrapper, 'is_method', True)
            return wrapper
        return maker

    def as_dictionaries(self, look4empty, query, *args, **kwargs):
        """ Результат выборки в виде списка словарей
            :param look4empty: признак игнорирования пустой выборки
            :param query: текст SQL запроса
            :param args: переменные, подставляемые в текст запроса
            :param kwargs: служебный словарь для сохранения результатов выборки
        """
        return CustomManager.as_dictionaries(
            self.make_query(query, *args, **kwargs), look4empty)

    def dictionaries(self, query, look4empty=False):
        """ Результат выборки в виде списка словарей
            :param query: текст SQL запроса (параметр декоратора)
            :param look4empty: признак игнорирования пустой выборки
        """
        def maker(function):
            is_instance = 'self' in function.func_code.co_varnames

            @wraps(function)
            def wrapper(*args, **kwargs):
                result = CustomManager.as_dictionaries(
                    self._middleware(is_instance, query, *args), look4empty)
                kwargs['result'] = result
                return function(*args, **kwargs)

            if is_instance:
                setattr(wrapper, 'is_method', True)
            return wrapper
        return maker

    def as_dictionary(self, look4empty, query, *args, **kwargs):
        """ Результат выборки в виде словаря
            :param look4empty: признак игнорирования пустой выборки
            :param query: текст SQL запроса
            :param args: переменные, подставляемые в текст запроса
            :param kwargs: служебный словарь для сохранения результатов выборки
        """
        return CustomManager.as_dictionary(
            self.make_query(query, *args, **kwargs), look4empty)

    def dictionary(self, query, look4empty=False):
        """ Результат выборки в виде словаря
            :param query: текст SQL запроса
            :param look4empty: признак игнорирования пустой выборки
        """
        def maker(function):
            is_instance = 'self' in function.func_code.co_varnames

            @wraps(function)
            def wrapper(*args, **kwargs):
                result = CustomManager.as_dictionary(
                    self._middleware(is_instance, query, *args), look4empty)
                kwargs['result'] = result
                return function(*args, **kwargs)

            if is_instance:
                setattr(wrapper, 'is_method', True)
            return wrapper
        return maker

    def as_generator_of_tuples(self, query, *args, **kwargs):
        """ Результат выборки в виде генератора кортежей
            :param query: текст SQL запроса
            :param args: переменные, подставляемые в текст запроса
            :param kwargs: служебный словарь для сохранения результатов выборки
        """
        return CustomManager.as_generator_of_tuples(
            self.make_query(query, *args, **kwargs))

    def generator_of_tuples(self, query):
        """ Результат выборки в виде генератора кортежей
            :param query: текст SQL запроса (параметр декоратора)
        """
        def maker(function):
            is_instance = 'self' in function.func_code.co_varnames

            @wraps(function)
            def wrapper(*args, **kwargs):
                result = CustomManager.as_generator_of_tuples(
                    self._middleware(is_instance, query, *args))
                kwargs['result'] = result
                return function(*args, **kwargs)

            if is_instance:
                setattr(wrapper, 'is_method', True)
            return wrapper
        return maker

    def as_tuples(self, look4empty, query, *args, **kwargs):
        """ Результат выборки в виде списка кортежей
            :param look4empty: признак игнорирования пустой выборки
            :param query: текст SQL запроса
            :param args: переменные, подставляемые в текст запроса
            :param kwargs: служебный словарь для сохранения результатов выборки
        """
        return CustomManager.as_tuples(
            self.make_query(query, *args, **kwargs), look4empty)

    def tuples(self, query, look4empty=False):
        """ Результат выборки в виде списка кортежей
            :param query: текст SQL запроса (параметр декоратора)
            :param look4empty: признак игнорирования пустой выборки
        """
        def maker(function):
            is_instance = 'self' in function.func_code.co_varnames

            @wraps(function)
            def wrapper(*args, **kwargs):
                result = CustomManager.as_tuples(
                    self._middleware(is_instance, query, *args), look4empty)
                kwargs['result'] = result
                return function(*args, **kwargs)

            if is_instance:
                setattr(wrapper, 'is_method', True)
            return wrapper
        return maker

    def as_tuple(self, look4empty, query, *args, **kwargs):
        """ Результат выборки в виде кортежа
            :param look4empty: признак игнорирования пустой выборки
            :param query: текст SQL запроса
            :param args: переменные, подставляемые в текст запроса
            :param kwargs: служебный словарь для сохранения результатов выборки
        """
        return CustomManager.as_tuple(
            self.make_query(query, *args, **kwargs), look4empty)

    def tuple(self, query, look4empty=False):
        """ Результат выборки в виде
            :param query: текст SQL запроса (параметр декоратора)
            :param look4empty: признак игнорирования пустой выборки
        """
        def maker(function):
            is_instance = 'self' in function.func_code.co_varnames

            @wraps(function)
            def wrapper(*args, **kwargs):
                result = CustomManager.as_tuple(
                    self._middleware(is_instance, query, *args), look4empty)
                kwargs['result'] = result
                return function(*args, **kwargs)

            if is_instance:
                setattr(wrapper, 'is_method', True)
            return wrapper
        return maker

    def as_value(self, look4empty, query, *args, **kwargs):
        """ Результат выборки в виде атомарного значения
            (первая колонка первой строки)
            :param look4empty: признак игнорирования пустой выборки
            :param query: текст SQL запроса
            :param args: переменные, подставляемые в текст запроса
            :param kwargs: служебный словарь для сохранения результатов выборки
        """
        return CustomManager.as_value(
            self.make_query(query, *args, **kwargs), look4empty)

    def value(self, query, look4empty=False):
        """ Результат выборки в виде атомарного значения
            :param query: текст SQL запроса (параметр декоратора)
            :param look4empty: признак выполнения пустой выборки
        """
        def maker(function):
            is_instance = 'self' in function.func_code.co_varnames

            @wraps(function)
            def wrapper(*args, **kwargs):
                result = CustomManager.as_value(
                    self._middleware(is_instance, query, *args), look4empty)
                kwargs['result'] = result
                return function(*args, **kwargs)

            if is_instance:
                setattr(wrapper, 'is_method', True)
            return wrapper
        return maker


class DynamicDataManager(DynamicBaseQuery):
    """ Модель динамических запросов с менеджером обработки данных """
    def __init__(self, connection):
        super(DynamicDataManager, self).__init__(connection)

    def _middleware(self, function, *args, **kwargs):
        """ Промежуточный этап декорирования, определение типа вызываемого
            объекта (функция или метод)
        """
        table = args[-1]
        result = self.make_select(table, **kwargs)
        return (args[0], result) \
            if 'self' in function.func_code.co_varnames else (None, result)

    def as_generator_of_dictionaries(self, table, schema='public', items=None,
                                     orders=None, conditions=None):
        """ Результат выборки в виде генератора словарей
            :param table: имя таблицы (представления и т.п.)
            :param schema: имя схемы
            :param items: список колонок на выборку
            :param orders: условия сортировки
            :param conditions: условия выборки
        """
        return CustomManager.as_generator_of_dictionaries(
            self.make_select(table, schema, items, orders, conditions))

    def generator_of_dictionaries(self, function):
        """ Результат выборки в виде генератора словарей
            :param function: декорируетый объект
        """
        @wraps(function)
        def wrapper(*args, **kwargs):
            obj, result = self._middleware(function, *args, **kwargs)
            result = CustomManager.as_generator_of_dictionaries(result)
            kwargs['result'] = result
            return function(*args, **kwargs)
        return wrapper

    def as_dictionaries(self, table, schema='public', items=None,
                        orders=None, conditions=None, look4empty=False):
        """ Результат выборки в виде списка словарей
            :param table: имя таблицы (представления и т.п.)
            :param schema: имя схемы
            :param items: список колонок на выборку
            :param orders: условия сортировки
            :param conditions: условия выборки
            :param look4empty: признак игнорирования пустой выборки
        """
        return CustomManager.as_dictionaries(
            self.make_select(
                table, schema, items, orders, conditions), look4empty)

    def dictionaries(self, look4empty=False):
        """ Результат выборки в виде списка словарей
            :param look4empty: признак игнорирования пустой выборки
                (параметр декоратора)
        """
        def refinement(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                obj, result = self._middleware(function, *args, **kwargs)
                result = CustomManager.as_dictionaries(result, look4empty)
                kwargs['result'] = result
                return function(*args, **kwargs)
            return wrapper
        return refinement

    def as_dictionary(self, table, schema='public', items=None, orders=None,
                      conditions=None, look4empty=False):
        """ Результат выборки в виде одиночного словаря
            :param table: имя таблицы (представления и т.п.)
            :param schema: имя схемы
            :param items: список колонок на выборку
            :param orders: условия сортировки
            :param conditions: условия выборки
            :param look4empty: признак игнорирования пустой выборки
        """
        return CustomManager.as_dictionary(
            self.make_select(
                table, schema, items, orders, conditions), look4empty)

    def dictionary(self, look4empty=False):
        """ Результат выборки в виде одиночного словаря
            :param look4empty: признак игнорирования пустой выборки
                (параметр декоратора)
        """
        def refinement(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                obj, result = self._middleware(function, *args, **kwargs)
                result = CustomManager.as_dictionary(result, look4empty)
                kwargs['result'] = result
                return function(*args, **kwargs)
            return wrapper
        return refinement

    def as_generator_of_tuples(self, table, schema='public', items=None,
                               orders=None, conditions=None):
        """ Результат выборки в виде генератора кортежей
            :param table: имя таблицы (представления и т.п.)
            :param schema: имя схемы
            :param items: список колонок на выборку
            :param orders: условия сортировки
            :param conditions: условия выборки
        """
        return CustomManager.as_generator_of_tuples(
            self.make_select(table, schema, items, orders, conditions))

    def generator_of_tuples(self, function):
        """ Результат выборки в виде генератора кортежей
            :param function: декорируемый объект
        """
        @wraps(function)
        def wrapper(*args, **kwargs):
            obj, result = self._middleware(function, *args, **kwargs)
            result = CustomManager.as_generator_of_tuples(result)
            kwargs['result'] = result
            return function(*args, **kwargs)
        return wrapper

    def as_tuples(self, table, schema='public', items=None, orders=None,
                  conditions=None, look4empty=False):
        """ Результат выборки в виде списка кортежей
            :param table: имя таблицы (представления и т.п.)
            :param schema: имя схемы
            :param items: список колонок на выборку
            :param orders: условия сортировки
            :param conditions: условия выборки
            :param look4empty: признак игнорирования пустой выборки
        """
        return CustomManager.as_tuples(
            self.make_select(
                table, schema, items, orders, conditions), look4empty)

    def tuples(self, look4empty=False):
        """ Результат выборки в виде списка кортежей
            :param look4empty: признак игнорирования пустой выборки
                (параметр декоратора)
        """
        def refinement(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                obj, result = self._middleware(function, *args, **kwargs)
                result = CustomManager.as_tuples(result, look4empty)
                kwargs['result'] = result
                return function(*args, **kwargs)
            return wrapper
        return refinement

    def as_tuple(self, table, schema='public', items=None, orders=None,
                 conditions=None, look4empty=False):
        """ Результат выборки в виде одиночного кортежа
            :param table: имя таблицы (представления и т.п.)
            :param schema: имя схемы
            :param items: список колонок на выборку
            :param orders: условия сортировки
            :param conditions: условия выборки
            :param look4empty: признак игнорирования пустой выборки
        """
        return CustomManager.as_tuple(
            self.make_select(
                table, schema, items, orders, conditions), look4empty)

    def tuple(self, look4empty=False):
        """ Результат выборки в виде одиночного кортежа
            :param look4empty: признак игнорирования пустой выборки
                (параметр декоратора)
        """
        def refinement(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                obj, result = self._middleware(function, *args, **kwargs)
                result = CustomManager.as_tuple(result, look4empty)
                kwargs['result'] = result
                return function(*args, **kwargs)
            return wrapper
        return refinement

    def as_value(self, table, schema='public', items=None, orders=None,
                 conditions=None, look4empty=False):
        """ Результат выборки в виде атомарного значения (первая колонка
            первой строки)
            :param table: имя таблицы (представления и т.п.)
            :param schema: имя схемы
            :param items: список колонок на выборку
            :param orders: условия сортировки
            :param conditions: условия выборки
            :param look4empty: признак игнорирования пустой выборки
        """
        return CustomManager.as_value(
            self.make_select(
                table, schema, items, orders, conditions), look4empty)

    def value(self, look4empty=False):
        """ Результат выборки в виде атомарного значения
            (первая колонка первой строки)
            :param look4empty: признак игнорирования пустой выборки
                (параметр декоратора)
        """
        def refinement(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                obj, result = self._middleware(function, *args, **kwargs)
                result = CustomManager.as_value(result, look4empty)
                kwargs['result'] = result
                return function(*args, **kwargs)
            return wrapper
        return refinement
