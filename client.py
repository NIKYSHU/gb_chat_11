import logging
import socket
import sys
import time
import project_logs.config.client_logs_config

from common.constants import *
from common.utils import *
from decors import Log


class Client:
    CLIENT_LOGGER = logging.getLogger('client_logger')

    def __init__(self, account_name='Guest', server_address=DEFAULT_IP_ADDRESS,
                 server_port=DEFAULT_PORT, client_mode='send'):
        self.server_address = server_address
        self.server_port = int(server_port)
        self.account_name = account_name
        self.client_mode = client_mode

    @Log()
    def create_presence(self):
        out_mes = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.account_name
            }
        }
        self.CLIENT_LOGGER.debug('Presence created')
        return out_mes

    @Log()
    def receive_message(self, message):
        if ACTION in message and message[ACTION] == MESSAGE and SENDER in message \
                and MESSAGE_TEXT in message:
            print(f'Message from {message[SENDER]}: {message[MESSAGE_TEXT]}')
            self.CLIENT_LOGGER.info(f'Message from {message[SENDER]}: {message[MESSAGE_TEXT]}')
        else:
            self.CLIENT_LOGGER.error(f'Invalid message from server: {message}')

    def create_message(self, sock):

        message = input(f'Input message or exit to exit: ')
        if message == 'exit':
            sock.close()
            self.CLIENT_LOGGER.info(f'Client close connection')
            sys.exit(0)
        message_dict = {
            ACTION: MESSAGE,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name,
            MESSAGE_TEXT: message
        }
        self.CLIENT_LOGGER.info(f'Message dict created: {message_dict}')
        return message_dict

    @Log()
    def answer_handler(self, message):
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return 'OK'
            return f'400 : {message[ERROR]}'
        self.CLIENT_LOGGER.critical('Invalid message')
        raise ValueError

    def main(self):
        if self.server_port < 1024 or self.server_port > 65535:
            raise ValueError
        self.CLIENT_LOGGER.info(f'Client created, Account: {self.account_name}')
        try:
            transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            transport.connect((self.server_address, self.server_port))
            send_message(transport, self.create_presence())
            answer = self.answer_handler(get_message(transport))
            self.CLIENT_LOGGER.info(f'Connected. Server answer: {answer}')
            print('Connected')
        except:
            self.CLIENT_LOGGER.error(f'Connection error')
            sys.exit(1)
        else:
            if self.client_mode == 'send':
                print('Sending messages')
            else:
                print('Receiving messages')

            while True:
                if self.client_mode == 'send':
                    try:
                        send_message(transport, self.create_message(transport))
                    except:
                        self.CLIENT_LOGGER.error('Connection refused')
                        sys.exit(1)
                if self.client_mode == 'listen':
                    try:
                        self.receive_message(get_message(transport))
                    except:
                        self.CLIENT_LOGGER.error('Connection refused')
                        sys.exit(1)


if __name__ == '__main__':
    try:
        if sys.argv[1]:
            DEFAULT_IP_ADDRESS = sys.argv[1]
        if sys.argv[2]:
            DEFAULT_PORT = sys.argv[2]
    except:
        pass
    client = Client(client_mode=input('Client mode (send, listen): '))
    client.main()
