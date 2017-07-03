# -*- coding: utf-8 -*-
""" Shoe2
    Анти-ORM пакет для работы с базами данных PostgreSQL
    Класс управления транзакциями
"""
from custom_errors import TransactionError


class Transaction(object):
    """ Класс, управляющий транзакционным блоком
        Реализован в виде примешиваемого класса (mixin-class)
    """
    def __init__(self):
        self.is_opened = False

    def begin(self):
        """ Открытие транзакционного блока """
        if self.is_opened:
            raise TransactionError(type=1).\
                describe(u"Предыдущая транзакция не завершена")

        try:
            self.run_query("begin")
        except StandardError, s_err:
            raise TransactionError(*s_err.args, type=3)\
                .describe(u"Не удалось открыть транзакцию")
        else:
            self.is_opened = True

    def commit(self):
        """ Подтверждение транзакции """
        if not self.is_opened:
            raise TransactionError(type=2).describe(u"Транзакция не открыта")

        try:
            self.run_query("commit")
        except StandardError, s_err:
            raise TransactionError(*s_err.args, type=3)\
                .describe(u"Не удалось завершить транзакцию")
        else:
            self.is_opened = False

    def rollback(self):
        """ Откат транзакции """
        if not self.is_opened:
            raise TransactionError(type=2).describe(u"Транзакция не открыта")

        try:
            self.run_query("rollback")
        except StandardError, s_err:
            raise TransactionError(*s_err.args, type=3)\
                .describe(u"Не удалось откатить транзакцию")
        else:
            self.is_opened = False
