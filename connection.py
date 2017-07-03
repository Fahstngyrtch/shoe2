# -*- coding: utf-8 -*-
""" Shoe2
    Анти-ORM пакет для работы с базами данных PostgreSQL
    Классы подключения к хранилищу данных и управления транзакциями
"""
import threading

import content
from custom_errors import ConnectionError, RunQueryError

if content.MARKER is None:
    raise ConnectionError(type=0).\
        describe(u"Перед исползованием пакета "
                 u"необходимо указать тип подключения")

Connection = content.MARKER


class ConnectionClass(object):
    """ Реализация разделяемого подключения к базе данных """
    __counter = 0
    locker = threading.Lock()
    db_conn = None

    @classmethod
    def __inc(cls):
        """ Счетчик подкючений, увеличение значения """
        cls.__counter += 1

    @classmethod
    def __dec(cls):
        """ Счетчик подкючений, уменьшение значения """
        cls.__counter -= 1

    @classmethod
    def connect(cls, db_name, user, password, host, port):
        """ Разделяемое подключение создается один раз методами класса
            и доступно для всех объектов данного класса
            :param db_name: наименование базы данных
            :param user: имя пользователя
            :param password: пароль
            :param host: хост
            :param port: номер порта
        """
        if not cls.db_conn:
            try:
                cls.db_conn = Connection(db_name, user, password, host, port)
                cls.db_conn.connect()
            except Exception as err:
                raise ConnectionError(*err.args, type=2).\
                    describe(u"Не удалось открыть соединение")
        return cls

    def disconnect(self):
        """ Разделяемое подключение нельзя закрывать явным образом.
            Закрытие соединения происходит только в деструкторе,
            когда счетчик подключений равен 1 (наш объект - последний)
        """

    def __init__(self, *args):
        """ Открытие подключения, если оно еще не открыто,
            и увеличение числа подключений
        """
        if not self.db_conn:
            self.connect(*args)

        with self.locker:
            self.__inc()

    def __del__(self):
        """ Уменьшение значения счетчика подключений.
            Если объект последний, то закрываем соединение
        """
        with self.locker:
            if self.__counter == 1:
                self.db_conn.disconnect()
                self.db_conn = None

    def run_query(self, query_string):
        """ Выполнение SQL запроса
            :param query_string: строка запроса
        """
        err, res = None, None
        if self.db_conn:
            with self.locker:
                try:
                    res = self.db_conn.run_query(query_string)
                except Exception as exc:
                    err = RunQueryError(exc.args, type=1).\
                        describe(u"Ошибка выполнения запроса")
            if err:
                raise err
            return res

        raise ConnectionError(type=1).describe(u"Соединение не открыто")


class ConnectionInstance(Connection):
    """ Реализация отдельного подключения на уровне экземпляра класса """
    def __init__(self, db_name, user, password, host, port):
        super(ConnectionInstance, self).__init__(db_name, user, password,
                                                 host, port)
        self.connect()

    def __del__(self):
        self.disconnect()


class Capstone(object):
    """ Фабрика объектов. Класс-обертка над различными типами подключения:
        отдельное подключение или общее.
        Экземпляр класса при вызове порождает объекты,
        реализующие тот тип подключения, который был задан в конструкторе класса
    """
    def __init__(self, conn_type, db_name, user, password, host, port):
        self.__db_name = db_name
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port

        if conn_type:
            self.__class = ConnectionInstance
        else:
            class ConnectionDummy(ConnectionClass):
                """ Шаблон класса для использования разделяемого подключения """
                __counter = 0
                LOCKER = threading.Lock()
                db_conn = None
                conn_atts = None

            self.__class = ConnectionDummy
            self.__class.connect(self.__db_name, self.__user, self.__password,
                                 self.__host, self.__port)

    def __call__(self):
        """ Объекты, реализующее подключение к базе данных,
            порождаются путем вызова экземпляра класса
        """
        return self.__class(self.__db_name, self.__user, self.__password,
                            self.__host, self.__port)
