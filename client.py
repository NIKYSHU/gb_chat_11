import sys
import json
import socket
import time
import logging
import log.config.client_log_config
from decor import Log


C_LOGGER = logging.getLogger('client')


@Log()
def presence(user):
    output = {
        "action": "presence",
        "time": time.time(),
        "user": {"account_name": user}
    }
    C_LOGGER.debug(f'Сформировано сообщение для пользователя {user}')
    return output


@Log()
def send_message(host, port):
    C_LOGGER.debug(f'Отправкеа сообщения: сервер {host}, порт {port}')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    send_msg = presence("user")
    json_send_msg = json.dumps(send_msg)
    encoded_msg = json_send_msg.encode("utf-8")
    s.send(encoded_msg)
    return s


@Log()
def get_message(socketsession):
    C_LOGGER.debug(f'Попытка получения сообщения {socketsession}')
    encoded_resp = socketsession.recv(1024)
    if isinstance(encoded_resp, bytes):
        json_resp = encoded_resp.decode("utf-8")
        resp = json.loads(json_resp)
        if isinstance(resp, dict):
            C_LOGGER.info(f'Принят ответ от сервера {resp}')
            return resp
        C_LOGGER.error(f'Не удалось декодировать сообщение сервера')
        raise ValueError
    C_LOGGER.error(f'Не удалось декодировать сообщение сервера')
    raise ValueError


@Log()
def get_answer(answer):
    C_LOGGER.debug(f'Обработка ответа сервера {answer}')
    if "response" in answer:
        if answer["response"] == 200:
            return '200 : OK'
        return f'400 : {answer["error"]}'
    C_LOGGER.error(f'Не удалось обработать ответ сервера')
    raise ValueError


def main():
    try:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_host = "127.0.0.1"
        server_port = 7777
    except ValueError:
        C_LOGGER.critical(f'Попытка запуска клиента с неподходящим номером порта {server_port}')
        sys.exit(1)
    C_LOGGER.info(f'Запущен клиент: сервер {server_host} и порт {server_port}')
    S = send_message(server_host, server_port)
    get_answer(get_message(S))


if __name__ == '__main__':
    main()
