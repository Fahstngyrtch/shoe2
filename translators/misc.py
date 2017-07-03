# -*- coding: utf-8 -*-
""" Shoe2
    Анти-ORM пакет для работы с базами данных PostgreSQL
    Набор функций для преобразования дат и времени
"""
import re
import time
import datetime

DATE_TEMPLATE = re.compile('[-, .]')
TIME_TEMPLATE = re.compile('[:.]')


def make_date(s_date, translate=True):
    """ Преобразует переменную s_date в тип date PostgreSQL или наоборот.
        :param s_date: переменная со значением даты. Это может быть строка,
            python-кортеж timetuple или экземпляр класса datetime.date
        :param translate: флаг, задающий направление трансформации.
            Если флаг поднят, то выполняется преобразование python -> PostgreSQL
        :returns datetime.date, если флаг сброшен, иначе строковое представление
            даты для PostgreSQL в формате "ДД.ММ.ГГГГ"
    """
    err_message = u"Неверный формат даты"
    if not s_date:
        if translate:
            return 'NULL'
        return None

    date_format = '%d.%m.%Y'
    if isinstance(s_date, datetime.date):
        arg = s_date
    elif isinstance(s_date, datetime.datetime):
        arg = datetime.date(s_date.year, s_date.month, s_date.day)
    elif isinstance(s_date, time.struct_time):
        arg = datetime.date(*s_date[:3])
    elif isinstance(s_date, (str, unicode)):
        lst = re.split(DATE_TEMPLATE, s_date)
        if not lst:
            raise ValueError(err_message)

        # Предполагаем, что значение задано в формате ГГ(ГГ)ММДД
        if len(lst) == 1:
            try:
                date_format = '%Y%m%d' if len(lst[0]) == 8 else '%y%m%d'
                year, month, day = [int(p) for p in time.strptime(
                    lst[0], date_format)[:3]]
            except StandardError:
                raise ValueError(err_message)
        else:
            try:
                day, month, year = [int(p) for p in lst]
            except StandardError:
                raise ValueError(err_message)
            if len(str(year)) < 4:
                # преобразование короткого года в полный
                year += (datetime.date.today().year / 1000) * 1000
        try:
            arg = datetime.date(year, month, day)
        except StandardError:
            raise ValueError(err_message)
    else:
        raise TypeError(u"Невозможно получить дату из {0}".format(s_date))

    if translate:
        return arg.strftime(date_format)
    return arg


def make_time(s_time, translate=True):
    """ Преобразует переменную s_time в тип time PostgreSQL или наоборот
        :param s_time: значение времени. Может быть представлен строкой,
            python-кортежем timetuple или объектом типа datetime.time
        :param translate: флаг, задающий направление трансформации.
            Если флаг поднят, то выполняется преобразование python -> PostgreSQL
        :returns объект типа datetime.time, если флаг сброшен, или строковое
            представление типа time PostgreSQL в формате ЧЧ:ММ:СС
    """
    err_message = u"Неверный формат времени"
    if not s_time:
        if translate:
            return 'NULL'
        return None

    time_format = '%H:%M:%S'
    if isinstance(s_time, datetime.time):
        arg = s_time
    elif isinstance(s_time, datetime.datetime):
        arg = datetime.time(s_time.hour, s_time.minute, s_time.second)
    elif isinstance(s_time, time.struct_time):
        arg = datetime.time(*s_time[3:6])
    elif isinstance(s_time, (str, unicode)):
        lst = re.split(TIME_TEMPLATE, s_time)
        if not lst:
            raise ValueError(err_message)

        try:
            lst_time = [int(p) for p in lst]
        except StandardError:
            raise ValueError(err_message)

        if len(lst_time) == 2:
            try:
                arg = datetime.time(lst_time[0], lst_time[1])
            except StandardError:
                raise ValueError(err_message)
            time_format = '%H:%M'
        elif len(lst_time) == 3:
            try:
                arg = datetime.time(lst_time[0], lst_time[1], lst_time[2])
            except StandardError:
                raise ValueError(err_message)
        else:
            raise ValueError(err_message)
    else:
        raise TypeError(u"Невозможно получить время из {0}".format(s_time))

    if translate:
        return arg.strftime(time_format)
    return arg


def make_datetime(s_datetime, translate=True, delimiter=' '):
    """ Преобразует значение s_datetime в тип timestamp PostgreSQL или наоборот
        :param s_datetime: дата-время. Может быть представлена в виде строки,
            python-кортежа timetuple или объекта типа datetime.datetime
        :param translate: флаг, задающий направление трансформации.
            Если флаг поднят, выполняется преобразование python -> PostgreSQL
        :param delimiter: символ(ы), разделения значения на дату и время.
        :returns объект типа datetime.datetime, если флаг сброшен, иначе
            текстовое представление timestamp PostgreSQL
            в формате  'ДД.ММ.ГГГГ ЧЧ:ММ:СС'
    """
    if not s_datetime:
        if translate:
            return 'NULL'
        return None
    if isinstance(s_datetime, datetime.datetime):
        arg = s_datetime
    elif isinstance(s_datetime, time.struct_time):
        arg = datetime.datetime(*s_datetime[:6])
    elif isinstance(s_datetime, (str, unicode)):
        s_date, s_time = s_datetime.split(delimiter)
        s_date, s_time = make_date(s_date, False), make_time(s_time, False)
        arg = datetime.datetime(s_date.year, s_date.month, s_date.day,
                                s_time.hour, s_time.minute, s_time.second)
    else:
        raise TypeError(u"Невозможно получить дату-время из {0}".format(
            s_datetime))

    datetime_format = "%d.%m.%Y %H:%M:%S"
    if translate:
        return arg.strftime(datetime_format)
    return arg


def make_interval(s_interval, translate=True):
    """ Преобразует значение s_interval в тип interval PostgreSQL или наоборот
        :param s_interval: заданный интервал. Может задаваться строкой, целым
            числом или объектом типа datetime.timedelta
        :param translate: флаг, задающий направление преобразования. Если флаг
            поднят, то выполняется трансформация python -> PostgreSQL
        :returns объект типа datetime.timedelta, если флаг сброшен, иначе
            строковое представление типа timedelta PostgreSQL (в секундах)
    """
    err_message = u"Невозможно получить интервал из {0}"
    if not s_interval:
        if translate:
            return 'NULL'
        return None

    if isinstance(s_interval, datetime.timedelta):
        arg = s_interval
    elif isinstance(s_interval, int):
        arg = datetime.timedelta(hours=s_interval)
    elif isinstance(s_interval, (str, unicode)):
        if ":" in s_interval:
            args = {}
            parts = ["seconds", "minutes", "hours"]
            for idx, item in enumerate(s_interval.split(":")[::-1][:3]):
                args[parts[idx]] = int(item)
            arg = datetime.timedelta(**args)
        else:
            args = {}
            num = re.search('\d+', s_interval)
            if num:
                num = num.group()
                if "{0} week".format(num) in s_interval:
                    args["weeks"] = int(num)
                elif "{0} day".format(num) in s_interval:
                    args["days"] = int(num)
                elif "{0} hour".format(num) in s_interval:
                    args["hours"] = int(num)
                elif "{0} minute".format(num) in s_interval:
                    args["minutes"] = int(num)
                elif "{0} second".format(num) in s_interval:
                    args["seconds"] = int(num)
                else:
                    raise ValueError(err_message.format(s_interval))
                arg = datetime.timedelta(**args)
            else:
                raise ValueError(err_message.format(s_interval))
    else:
        raise TypeError(err_message.format(s_interval))

    if translate:
        return "{0} second".format(int(arg.total_seconds()))
    return arg
