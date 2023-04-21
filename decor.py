import inspect
import logging
import sys
import traceback

if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


class Log:
    def __call__(self, func):
        def create_log(*args, **kwargs):
            ret = func(*args, **kwargs)
            LOGGER.debug(f'Функция {func.__name__} c параметрами {args}, {kwargs}. '
                         f'Вызов из модуля {func.__module__}.'
                         f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}.'
                         f'Вызов из функции {inspect.stack()[1][3]}')
            return ret
        return create_log