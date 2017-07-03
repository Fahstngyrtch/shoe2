# -*- coding: utf-8 -*-
""" Shoe2
    Анти-ORM пакет для работы с базами данных PostgreSQL
    Работа с хранилищем данных на основе драйвера DB-API 2
"""
import pg

import content
from transaction import Transaction
from custom_errors import ConnectionError, RunQueryError


class PgWrapper(Transaction):
    """ Обертка над драйвером DB-API 2 """
    def __init__(self, db_name, user, password, host, port):
        """ Конструктор класса
        :param db_name: наименование базы данных
        :param user: имя пользователя
        :param password: пароль
        :param host: хост
        :param port: номер порта
        """
        super(PgWrapper, self).__init__()
        self.__conn = None

        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def __del__(self):
        """ Отсоединяемся от базы, если пользователь сам забыл это сделать """
        self.disconnect()

    def connect(self):
        """ Открытие соединения с базой """
        try:
            self.__conn = pg.DB(dbname=self.db_name, user=self.user,
                                passwd=self.password, host=self.host,
                                port=self.port)
        except StandardError as err:
            raise ConnectionError(*err.args).\
                describe(u"Невозможно выполнить подключение")

    def disconnect(self):
        """ Закрываем соединение """
        if self.__conn:
            try:
                self.__conn.close()
            except:
                pass

    def run_query(self, query):
        """ Выполнение запроса на открытом соединении
            :param query: текст запроса
        """
        if isinstance(query, unicode):
            query = query.encode('utf-8')
        else:
            raise RunQueryError().describe(u"Ошибка выполнения запроса")

        try:
            result = self.__conn.query(query)
        except pg.Error as err:
            raise RunQueryError(*err.args).\
                describe(u"Ошибка выполнения запроса")
        else:
            if type(result).__name__ == 'pgqueryobject':
                fields = result.listfields()
                return [content.DataContainer(fields, i)
                        for i in result.getresult()]
            else:
                if result is None:
                    result = 0

                return [content.DataContainer(None, None, result), ]

content.MARKER = PgWrapper

# импорт модуля происходит в самом конце для инициализации выбранного
# разработчиком варианта подключения к базе данных
import connection
