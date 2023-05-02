"""Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса. По результатам проверки должно
выводиться соответствующее сообщение.
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
            host_reach.append(i)
        else:
            print(f'{i} - Узел недоступен')
            host_unreach.append(i)


def host_range_ping(addr,row):
    host = []
    i = ipaddress.ip_address(addr)
    last = int(addr.split('.')[3])
    if (last + int(row)) < 254:
        for a in range(row):
            host.append(str(i + a))
    else:
        print("Wrong range")
    host_ping(host)


if __name__ == '__main__':
    host_range_ping("192.168.0.192", 5)

"""
Результат:
192.168.0.192 - Узел доступен
192.168.0.193 - Узел доступен
192.168.0.194 - Узел доступен
192.168.0.195 - Узел доступен
192.168.0.196 - Узел доступен
"""