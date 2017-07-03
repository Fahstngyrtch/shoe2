# -*- coding: utf-8 -*-
""" Shoe2
    Анти-ORM пакет для работы с базами данных PostgreSQL
    Классы исключений
"""


class CustomError(StandardError):
    __err_code = 0

    def __init__(self, *args, **kwargs):
        super(CustomError, self).__init__(*args)
        self.__description = ""
        self.__err_type = kwargs.get("type")
        self.__err_code += kwargs.get("code") or 0

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def err_type(self):
        return self.__err_type

    @err_type.setter
    def err_type(self, value):
        self.__err_type = value

    def __str__(self):
        return "{0}: {1}\n{2}\n{3}".format(self.__err_code + self.err_type,
                                           self.description,
                                           self.message,
                                           self.args)

    def __unicode__(self):
        return u"{0}: {1}\n{2}\n{3}".format(self.__err_code + self.err_type,
                                            self.description,
                                            self.message,
                                            self.args)

    def __repr__(self):
        return "{0}: {1}".format(self.__err_code + self.err_type,
                                 self.description)

    def describe(self, message):
        self.description = message
        return self


class ConnectionError(CustomError):
    """ Ошибки подключения к базе данных """
    __err_code = 100


class MakeQueryError(CustomError):
    """ Ошибки формирования строки с запросом """
    __err_code = 200


class RunQueryError(CustomError):
    """ Ошибки выполнения запроса """
    __err_code = 300


class TransactionError(CustomError):
    """ Ошибки выполнения транзакции """
    __err_code = 400


class DataError(CustomError):
    """ Ошибки обработки данных """
    __err_code = 500
