import os
import sys
import logging


LOG_CLIENT = logging.getLogger("client")
format_msg = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')


PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, '../log/client.log')


clientlog_file = logging.FileHandler(PATH,encoding='utf8')


clientlog_file.setFormatter(format_msg)
hand_log = logging.StreamHandler(sys.stderr)
hand_log.setLevel(logging.WARNING)
hand_log.setFormatter(format_msg)


LOG_CLIENT.addHandler(hand_log)
LOG_CLIENT.addHandler(clientlog_file)
LOG_CLIENT.setLevel(logging.DEBUG)


if __name__ == '__main__':
    LOG_CLIENT.critical('Критическая ошибка')
    LOG_CLIENT.error('Ошибка')
    LOG_CLIENT.debug('Отладочная информация')
    LOG_CLIENT.info('Информационное сообщение')