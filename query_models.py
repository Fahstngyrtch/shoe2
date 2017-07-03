# -*- coding: utf-8 -*-
""" Shoe2
    Анти-ORM пакет для работы с базами данных PostgreSQL
    Классы построения динамических и статических SQL запросов
"""
from custom_errors import MakeQueryError, RunQueryError


class BaseQuery(object):
    """ Базовый класс построения и выполнения SQL запросов """
    def __init__(self, connection):
        """ Конструктор класса
            :param connection: открытое подключение к источнику данных
        """
        self.__conn = connection

    def raw_query(self, query):
        """ Выполнение SQL запроса из переданной строки
            :param query: строка с запросом
            :return: результат выполнения запроса
        """
        try:
            return self.__conn.run_query(query)
        except Exception as err:
            raise RunQueryError(*err.args)

    def begin(self):
        """ Открытие транзакции """
        self.__conn.begin()

    def commit(self):
        """ Завершение транзакции """
        self.__conn.commit()

    def rollback(self):
        """ Откат транзакции """
        self.__conn.rollback()

    @staticmethod
    def _prepare_query(query_string, *args, **kwargs):
        """ Подготовка SQL запроса к выполнению
            :param query_string: шаблон запроса (форматированная строка)
            :param args: позиционые аргументы для вставки в строку
            :param kwargs: именованные аргументы для вставки в строку
            :return: сформированная строка
        """
        try:
            if args:
                query_string = query_string % args
            elif kwargs:
                query_string = query_string % kwargs
        except Exception as err:
            raise MakeQueryError(*err.args)
        return query_string

    @staticmethod
    def as_dict(result):
        """ Возвращаем результат в виде списка словарей
            :param result: результат выполнения запроса
            :return: список словарей с результатом выборки
        """
        if result:
            for r in result:
                yield r.to_dict()
        else:
            yield None

    @staticmethod
    def as_tuple_(result):
        """ Возвращаем результат в виде списка кортежей
            :param result: результат выполнения запроса
            :return: список кортежей с результатом выборки
        """
        if result:
            for r in result:
                yield r.to_tuple()
        else:
            yield None


class StaticBaseQuery(BaseQuery):
    """ Выполнение шаблонных запросов """
    def __init__(self, connection):
        super(StaticBaseQuery, self).__init__(connection)

    def make_query(self, query, *args, **kwargs):
        query = self._prepare_query(query, *args, **kwargs)
        return self.raw_query(query)


class DynamicBaseQuery(BaseQuery):
    """ Динамическое формирование и выполнение SQL запросов """
    # Шаблоны запросов
    INSERT = "INSERT INTO %(schema)s.%(table)s %(columns)s VALUES %(values)s;"
    I_SELECT = "INSERT INTO %(schema)s.%(table)s %(columns)s %(select)s;"
    SELECT = "SELECT %(items)s FROM %(schemafrom)s.%(tablefrom)s " \
             "WHERE %(conditions)s"
    UPDATE = "UPDATE %(schema)s.%(table)s SET %(items)s WHERE %(conditions)s;"
    DELETE = "DELETE FROM %(schema)s.%(table)s WHERE %(conditions)s;"
    FULL_DELETE = "TRUNCATE TABLE %(schema)s.%(table)s;"

    def __init__(self, connection):
        super(DynamicBaseQuery, self).__init__(connection)

    def make_insert(self, table, schema='public', columns=None, values=None):
        """ Вставка строки в таблицу
            :param table: наименование таблицы
            :param schema: наименование схемы
            :param columns: список с именами колонок
            :param values: список со значениями
            :return: результат выполнения запроса
        """
        query = self.INSERT

        if not values:
            raise MakeQueryError(code=1).\
                describe(u"Недостаточно данных для записи")

        if not isinstance(values, (tuple, list)):
            raise MakeQueryError(code=2).\
                describe(u"Данные для записи передаются списком или кортежем")

        pattern = {'schema': schema or 'public', 'table': table,
                   'values': "(%s)" % values[0] if len(values) == 1
                   else "(%s)" % ",".join(["%s" % i for i in values])
                   }

        if columns:
            if not isinstance(columns, (list, tuple)):
                raise MakeQueryError(code=2).\
                    describe(u"Имена колонок передаются списком или кортежем")

            pattern['columns'] = "(%s)" % columns[0] if len(columns) == 1 \
                else "(%s)" % ",".join(columns)
        else:
            query = query.replace('%(columns)s', '')

        query = self._prepare_query(query, **pattern)
        return self.raw_query(query)

    def make_insert_from_select(self, insert_table, select_table,
                                insert_schema="public", select_schema="public",
                                insert_columns=None, select_items=None,
                                **kwargs):
        """ Выполнение встакки через SELECT запрос
            :param insert_table: имя таблицы для вставки
            :param select_table: имя таблицы-источника
            :param insert_schema: схема таблицы назначения
            :param select_schema: схема таблицы-источника
            :param insert_columns: список колонок на вставку
            :param select_items: список колонок на выборку
            :param kwargs: словарь с условиями выборки вида
                {имя колонки: (операция сравнения, сравниваемое значение)}
            :return: результат выполнения запроса
        """
        query = self.I_SELECT
        ins_pattern = {'schema': insert_schema or 'public',
                       'table': insert_table}

        if insert_columns:
            if not isinstance(insert_columns, (list, tuple)):
                raise MakeQueryError(code=2).\
                    describe(u"Имена колонок передаются списком или кортежем")

            ins_pattern['columns'] = "(%s)" % insert_columns[0] \
                if len(insert_columns) == 1 \
                else "(%s)" % ",".join(insert_columns)
        else:
            query = query.replace('%(columns)s', '')

        sel_pattern = {'schemafrom': select_schema or 'public',
                       'tablefrom': select_table}

        if select_items:
            if not isinstance(select_items, (list, tuple)):
                raise MakeQueryError(code=2).\
                    describe(u"Имена колонок передаются списком или кортежем")

            sel_pattern['items'] = "%s" % select_items[0] \
                if len(select_items) == 1 else ",".join(select_items)
        else:
            sel_pattern['items'] = "*"

        if not kwargs:
            sel_pattern['conditions'] = "1 = 1"
        else:
            sel_pattern['conditions'] = " AND ".join(["%s %s %s" % (key,
                                                                    value[0],
                                                                    value[1])
                                                      for key, value
                                                      in kwargs.items()])

        ins_pattern['select'] = self._prepare_query(self.SELECT, **sel_pattern)
        query = self._prepare_query(query, **ins_pattern)
        return self.raw_query(query)

    def make_select(self, table, schema='public', items=None,
                    orders=None, conditions=None):
        """ Выполнение SQL запроса на выборку
            :param table: имя таблицы
            :param schema: имя схемы
            :param items: имена полей таблицы
            :param orders: сортировка результата (для сортировки по убыванию
                имя предваряется символом '-')
            :param conditions: условия выборки {имя колонки: (операция
                сравнения, сравниваемое значение)}
            :return: результат выполнения запроса
        """
        pattern = {'schemafrom': schema or 'public', 'tablefrom': table}

        if items:
            pattern['items'] = "%s" % items[0] if len(items) == 1 \
                else ",".join([str(i) for i in items])
        else:
            pattern['items'] = "*"

        if not conditions:
            pattern['conditions'] = "1 = 1"
        else:
            if not isinstance(conditions, dict):
                raise MakeQueryError(code=2).\
                    describe(u"Условия выборки передаются в виде словаря")
            pattern['conditions'] = " AND ".join(["%s %s %s" % (key,
                                                                value[0],
                                                                value[1])
                                                  for key, value
                                                  in conditions.items()])
        if orders:
            order_by = " ORDER BY "
            items = []
            for item in orders:
                if item.stsartswith('-'):
                    items.append("{0} DESC".format(item[1:]))
                else:
                    items.append(item)
            order_by += ",".join([i for i in items]) + ";"
        else:
            order_by = ";"

        query = self.SELECT + order_by
        query = self._prepare_query(query, **pattern)
        return self.raw_query(query)

    def make_update(self, table, schema='public', *items, **conditions):
        """ Выполнение запроса на изменение записей по условию
            :param table: имя таблицы
            :param schema: имя схемы
            :param items: кортеж вида (имя колонки, значение)
            :param conditions: условия выборки {имя колонки: (операция
                сравнения, сравниваемое значение)}
            :return: результат выполнения запроса
        """
        if not items:
            raise MakeQueryError(code=1).\
                describe(u"Необходимо указать изменяемые атрибуты")

        pattern = {'schema': schema or 'public', 'table': table,
                   'items': ",".join(["%s = %s" % (i[0], i[1]) for i in items])}

        if not conditions:
            pattern['conditions'] = "1 = 1"
        else:
            if not isinstance(conditions, dict):
                raise MakeQueryError(code=2).\
                    describe(u"Условия выборки передаются в виде словаря")
            pattern['conditions'] = " AND ".join(["%s %s %s" % (key,
                                                                value[0],
                                                                value[1])
                                                  for key, value
                                                  in conditions.items()])

        query = self._prepare_query(self.UPDATE, **pattern)
        return self.raw_query(query)

    def make_delete(self, table, schema='public', **conditions):
        """ Удаление записей по условию
            :param table: имя таблицы
            :param schema: имя схемы
            :param conditions: условия {имя колонки: (операция сравнения,
                сравниваемое значение)}
            :return: результат выполнения запроса
        """
        pattern = {'schema': schema or 'public', 'table': table}
        if not conditions:
            pattern['conditions'] = "1 = 1"
        else:
            pattern['conditions'] = " AND ".join(["%s %s %s" % (key,
                                                                value[0],
                                                                value[1])
                                                  for key, value
                                                  in conditions.items()])

        query = self._prepare_query(self.DELETE, **pattern)
        return self.raw_query(query)

    def make_truncate(self, table, schema='public'):
        """ Полная очистка указанной таблицы
        :param table: имя таблицы
        :param schema: имя схемы
        :return: результат выполнения запроса
        """
        pattern = {'schema': schema or 'public', 'table': table}
        query = self._prepare_query(self.FULL_DELETE, **pattern)
        return self.raw_query(query)
