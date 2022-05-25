# coding=utf-8
from Utility.Path import path_join
from logging import handlers
from functools import wraps
from datetime import datetime
import logging
import traceback
import os


def initial_log(filename, stream=True, dir=''):
    # traceback.print_stack()
    logger = logging.getLogger(filename)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if logger.hasHandlers():  # or it will duplicate the log messages
        logger.handlers.clear()
    # file_handler = logging.FileHandler(filename=f'log/{filename}.log',encoding='utf-8')
    if stream:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    f_name = path_join('log', f'{filename}.log')
    if dir:
        f_name = os.path.join(dir, filename)
    try:
        dir_path = os.path.split(f_name)[0]
        os.makedirs(dir_path)
    except FileExistsError:
        pass
    file_handler = logging.handlers.RotatingFileHandler(filename=f_name, encoding='utf-8', maxBytes=2048000,
                                                        backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    logger.info('********    Enter log in initial_log      ********')

    return logger

    # logging.basicConfig(level=logging.DEBUG,
    #                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #                     filename='.log/'+filename+'.log')


class LogManager:
    def __init__(self):
        self.manager = {}

    def __call__(self, log_name, stream=False, dir=''):
        if log_name.find('.py') != -1:
            log_name = os.path.split(log_name)[1][:-3]
        if log_name not in self.manager:
            self.manager[log_name] = initial_log(log_name, stream=stream, dir=dir)  # TODO 如果dir不一樣的話就GG
        return self.manager[log_name]

    def log(self, log_name, isclass=True, stream=False, dir=''):
        if not self.manager.get(log_name, False):
            self.manager[log_name] = initial_log(log_name, stream=stream, dir=dir)

        def outer_wrapper(func):
            # print('in outer wrapper')

            @wraps(func)
            def wrapper(*args, **kwargs):
                # print('in wrapper')
                self.manager[log_name].debug(f'calling {func.__name__}: {args[1 if isclass else 0:]}{kwargs}')
                # print('in wrapper2')
                return func(*args, **kwargs)
            return wrapper
        return outer_wrapper


log_manager = LogManager()


class RaiseAfterLog:
    def __init__(self):
        self.logger = log_manager('Exception')

    def __call__(self):
        def outer_wrapper(func):
            # print('in outer wrapper')

            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except BaseException as e:
                    self.logger.debug(traceback.format_exc())
                    raise e
            return wrapper

        return outer_wrapper


RAL = RaiseAfterLog()


def is_log_level_valid(log_name, log, level='ERROR'):
    return log.find(f'- {log_name} - {level} -') != -1


def get_log(log_filename, level='ERROR'):
    """

    :param log_filename:
    :param level:
    :return: [(time, log), (time, log),...]
    """
    _, log_name = os.path.split(log_filename)
    log_name = log_name[:log_name.find('.')]
    previous_time = None
    previous_log = ''
    result = list()
    with open(log_filename, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                tmp_time = datetime.strptime(line[:23], '%Y-%m-%d %H:%M:%S,%f')
                if is_log_level_valid(log_name, previous_log, level=level):
                    result.append((previous_time, previous_log))
                previous_time = tmp_time
                previous_log = line
            except ValueError:
                previous_log += line
    if is_log_level_valid(log_name, previous_log, level=level):
        result.append((previous_time, previous_log))
    return result


if __name__ == "__main__":
    # @RAL()
    # def IWillError():
    #     error = 1/0
    #
    # # IWillError()
    #
    #
    # class ErrorClass:
    #     @RAL()
    #     def __init__(self):
    #         self.ll = 1
    #         self._error()
    #
    #     def _error(self):
    #         self.ll /= 0
    #
    # ErrorClass()

    # testlogger = LogManager()
    # testlogger('test').debug('lol')
    #
    # testlogger = initial_log('test')
    # testlogger.debug('hey debug')
    # testlogger.debug('我是中文唷')
    # testlogger.warning('hey warning')

    # path = path_join('log', 'ggg')
    # logger = log_manager('GGG', dir=path)
    # logger.debug('hello world')

    path = path_join('log', 'eMISvalueAction.log.1')
    count = 0
    for time, log in get_log(path, level='DEBUG'):
        print(time)
        print(log)
        print('-------------')
        count += 1
        if count == 20:
            break
