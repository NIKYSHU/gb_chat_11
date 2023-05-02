"""Продолжаем работать над проектом «Мессенджер»:
a. Реализовать скрипт, запускающий два клиентских приложения: на чтение чата и на
запись в него. Уместно использовать модуль subprocess);
b. Реализовать скрипт, запускающий указанное количество клиентских приложений.
"""

from subprocess import Popen, CREATE_NEW_CONSOLE


def main():
    p_list = []
    while True:
        user = input("Запустить N клиентов:  / Закрыть клиентов (x) / Выйти (q) ")
        if user == 'q':
            break
        elif user == 'x':
            while p_list:
                p_list.pop().kill()
        else:
            p_list.append(Popen("python server.py", creationflags=CREATE_NEW_CONSOLE))
            for i in range(int(user)):
                p_list.append(Popen('python client.py', creationflags=CREATE_NEW_CONSOLE))


if __name__ == "__main__":
    main()