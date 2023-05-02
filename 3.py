"""Написать функцию host_range_ping_tab(), возможности которой основаны на функции из
примера 2. Но в данном случае результат должен быть итоговым по всем ip-адресам,
представленным в табличном формате (использовать модуль tabulate). """

import subprocess
import ipaddress
from tabulate import tabulate


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
    return host_reach, host_unreach


def host_range_ping(addr,row):
    host = []
    i = ipaddress.ip_address(addr)
    last = int(addr.split('.')[3])
    if (last + int(row)) < 254:
        for a in range(row):
            host.append(str(i + a))
    else:
        print("Wrong range")
    return host_ping(host)


def host_range_ping_tab(addr, row):
    result1, result2 = host_range_ping(addr, row)
    result = {'Доступные узлы': "", 'Недоступные узлы': ""}
    for i in result1:
        result['Доступные узлы'] += f"{i}\n"
    for i in result2:
        result['Недоступные узлы'] += f"{i}\n"
    print(tabulate([result], headers='keys', tablefmt="pipe", stralign="center"))


if __name__ == '__main__':
    host_range_ping_tab("192.168.0.192", 5)

"""
192.168.0.192 - Узел доступен
192.168.0.193 - Узел доступен
192.168.0.194 - Узел доступен
192.168.0.195 - Узел доступен
192.168.0.196 - Узел доступен
|  Доступные узлы  |  Недоступные узлы  |
|:----------------:|:------------------:|
|  192.168.0.192   |                    |
|  192.168.0.193   |                    |
|  192.168.0.194   |                    |
|  192.168.0.195   |                    |
|  192.168.0.196   |                    |
"""