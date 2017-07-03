# -*- coding: utf-8 -*-
""" Shoe2
    Анти-ORM пакет для работы с базами данных PostgreSQL
    Класс-контейнер для хранения одного из кортежей, возвращаемых выборкой
"""
MARKER = None


class DataContainer(object):
    """ Класс-контейнер для различного представления выборки """
    def __init__(self, structure, content, *args):
        """ Конструктор класса
            :param structure: структура выборки (набор полей)
            :param content: кортеж (один элемент из выборки)
            :param args: дополнительные аргументы (счктчик столбцов )
        """
        self.__fieldnames = structure or ()
        self.__content = content or []
        self.__counter = args[0] if args else len(self.__content)

    def to_tuple(self):
        """ Преобразование к кортежу """
        return self.__content

    def to_dict(self):
        """ Преобразование к словарю """
        return dict(zip(self.__fieldnames, self.__content))

    @property
    def columns(self):
        """ Имена колонок """
        return self.__fieldnames

    @property
    def counter(self):
        """ Ширина выборки (количество столбцов) """
        return self.__counter
