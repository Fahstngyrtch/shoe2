# -*- coding: utf-8 -*-
""" Shoe2
    Анти-ORM пакет для работы с базами данных PostgreSQL
    Работа с хранилищем данных на основе psycopg2.
"""
import psycopg2 as psy
import psycopg2.extensions as exten

import content
from transaction import Transaction
from custom_errors import ConnectionError, RunQueryError

exten.register_type(exten.UNICODE)


class PsycoWrapper(Transaction):
    """ Обертка над драйвером psycopg2 """
    def __init__(self, db_name, user, password, host, port):
        """ Конструктор класса
        :param db_name: наименование базы данных
        :param user: имя пользователя
        :param password: пароль
        :param host: хост
        :param port: номер порта
        """
        super(PsycoWrapper, self).__init__()
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
            # SSL подключение по умолчанию не используется
            self.__conn = psy.connect(database=self.db_name, user=self.user,
                                      password=self.password, host=self.host,
                                      port=self.port, sslmode='disable')
        except StandardError as err:
            raise ConnectionError(*err.args).\
                describe(u"Невозможно выполнить подключение")
        self.__conn.set_isolation_level(exten.ISOLATION_LEVEL_AUTOCOMMIT)

    def disconnect(self):
        """ Закрываем соединение """
        if self.__conn and (not self.__conn.closed):
            self.__conn.close()

    def run_query(self, query):
        """ Выполнение запроса на открытом соединении
            :param query: текст запроса
        """
        cur = self.__conn.cursor()

        try:
            cur.execute(query)
        except StandardError as err:
            cur.close()
            raise RunQueryError(*err.args).\
                describe(u"Ошибка выполнения запроса")
        else:
            if "SELECT" in cur.statusmessage:
                struct = [i[0] for i in cur.description]
                data = cur.fetchall()
                result = [content.DataContainer(struct, i) for i in data]
            else:
                try:
                    count = int(cur.statusmessage.split(' ')[-1])
                except ValueError:
                    count = 0

                result = [content.DataContainer(None, None, count)]

            cur.close()
            return result

content.MARKER = PsycoWrapper

# импорт модуля происходит в самом конце для инициализации выбранного
# разработчиком варианта подключения к базе данных
import connection
