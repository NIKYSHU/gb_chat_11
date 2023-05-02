"""Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться
доступность сетевых узлов. Аргументом функции является список, в котором каждый сетевой
узел должен быть представлен именем хоста или ip-адресом. В функции необходимо
перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с
помощью функции ip_address().
"""

import subprocess
import ipaddress


def host_ping(host):

    host_reach = []
    host_unreach = []

    for i in host:
        try:
            i = ipaddress.ip_address(i)
        except:
            pass
        p = subprocess.Popen(f"ping -c 1 {i}", shell=False, stdout=subprocess.PIPE)
        p.wait()
        if p.returncode == 0:
            print(f'{i} - Узел доступен')
            host_reach.append(str(i))
        else:
            print(f'{i} - Узел недоступен')
            host_unreach.append(str(i))


if __name__ == '__main__':
    args = ['mail.ru', 'google.com', '2.2.2.2', '192.168.0.192']
    host_ping(args)


"""
Результат:
mail.ru - Узел доступен
google.com - Узел доступен
2.2.2.2 - Узел недоступен
192.168.0.192 - Узел доступен
"""
