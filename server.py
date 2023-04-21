import socket
import sys
import json
import logging
import log.config.server_log_config
from decor import Log


S_LOGGER = logging.getLogger('server')


@Log()
def get_msg(tr_socket):
    S_LOGGER.debug(f'Попытка получения сообщения: {tr_socket}')
    encoded_resp = tr_socket.recv(1024)
    if isinstance(encoded_resp, bytes):
        json_resp = encoded_resp.decode("utf-8")
        resp = json.loads(json_resp)
        if isinstance(resp, dict):
            S_LOGGER.info(f'Принято сообщение клиента {resp}')
            return resp
        S_LOGGER.error(f'Не удалось декодировать сообщение клиент')
        raise ValueError
    S_LOGGER.error(f'Не удалось декодировать сообщение клиент')
    raise ValueError


@Log()
def make_answer(answerclient: dict):
    S_LOGGER.debug(f'Проверка сообщения от клиента: {answerclient}')
    if "action" in answerclient and answerclient["action"] == "presence" and "time" in answerclient \
            and "user" in answerclient and answerclient["user"]["account_name"] == 'user':
        return {"response": 200}
    return {
        "response": 400,
        "error": 'Bad Request'
    }


@Log()
def send_msg(tr_socket, msgtoclient):
    S_LOGGER.debug(f'Отправка сообщения {msgtoclient} клиенту {tr_socket}')
    js_msg = json.dumps(msgtoclient)
    encoded_msg = js_msg.encode("utf-8")
    tr_socket.send(encoded_msg)


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = 7777
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        S_LOGGER.critical(f'Номер порта не указан')
        sys.exit(1)
    except ValueError:
        S_LOGGER.critical(f'Номер порта {listen_port} указан некорректно. Нужно указать в диапазоне 1024 - 65535')
        sys.exit(1)
    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        S_LOGGER.critical(f'Адрес не указан')
        sys.exit(1)
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.listen(5)
    S_LOGGER.info(f'Сервер запущен. порт: {listen_port}')
    while True:
        tr_socket, client_address = transport.accept()
        S_LOGGER.info(f'соединение установлено c {client_address}')
        message_from_client = get_msg(tr_socket)
        S_LOGGER.debug(f'Получено сообщение {message_from_client}')
        response = make_answer(message_from_client)
        S_LOGGER.info(f'Сформирован ответ {response}')
        send_msg(tr_socket, response)
        S_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается')
        tr_socket.close()


if __name__ == '__main__':
    main()