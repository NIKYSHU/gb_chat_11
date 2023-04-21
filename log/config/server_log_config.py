import sys
import os
import logging.handlers


LOGGER = logging.getLogger('server')
format_msg = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')


PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, '../log/server.log')


handler_log = logging.StreamHandler(sys.stderr)
handler_log.setFormatter(format_msg)
handler_log.setLevel(logging.ERROR)
LOGS = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
LOGS.setFormatter(format_msg)


LOGGER.addHandler(handler_log)
LOGGER.addHandler(LOGS)
LOGGER.setLevel(logging.DEBUG)


if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')