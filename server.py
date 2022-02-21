from dataclasses import dataclass
from collections import deque
import socket
import threading
import time
from typing import List
import sys
import os

task_queue = deque()
connections = dict()


@dataclass
class ClientInfo:
    ip: str
    port: str
    name: str
    connection: socket
    address: List


def dispatcher_thread(_task_queue: deque, all_connection):
    while True:
        time.sleep(1)
        if len(_task_queue) == 0:
            continue

        task = _task_queue.pop()

        try:

            if task['receiver'] not in all_connection.keys():
                _task_queue.appendleft(task)
                continue
            
            receiver: ClientInfo = all_connection.get(task['receiver'])
            receiver.connection.send(task['data'].encode('ascii'))

        except Exception as ex:
            print(f'exception in {dispatcher_thread} ', ex)
        
def socket_client_thread_receiver(tcp_connection, connection_address, _task_queue, all_connection):
    name = None
    while True:
        data = tcp_connection.recv(1024)

        # means client is lost
        if not data: 
            tcp_connection.close()
            print(f'client {name}({connection_address[0]}{connection_address[1]}) was closed.') 
            
            # remove clinet from list
            if name:
                all_connection.pop(name)

            break
        
        # process data
        text_data = str(data.decode('ascii'))
        text_data = text_data.split(',')

        command = text_data[0]

        if command == 'handshake':
            name = text_data[1]
            ip = connection_address[0]
            port = connection_address[1]
            all_connection[name] = ClientInfo(ip=ip, port=port, name=name,
                                              connection=tcp_connection, address=connection_address)
            print(f'client {name} is connected.')

        elif command == 'send':
            to = text_data[1]
            send_data = text_data[2]
            _task_queue.append({
                'receiver': to,
                'sender': name,
                'data': send_data
            })

        else:
            print(f'get unknow command from client {name} port {port}, command -> {command}')

def accept_socket_connection():
    port = 12347
    # 127.0.0.1
    host = ''
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((host,port))
    server_socket.listen(5)
    print('server is started ...')
    threading.Thread(target=dispatcher_thread, args=(task_queue, connections)).start()

    try:
        while True:
            tcp_connection, connection_address = server_socket.accept()
            # print('connected to -> ', connection_address[0], ':', connection_address[1])
            
            threading.Thread(target=socket_client_thread_receiver,
                             args=(tcp_connection, connection_address, task_queue, connections)).start()

    except Exception as ex:
        print(ex)
        server_socket.close()
    except KeyboardInterrupt:
        server_socket.close()
        print('server closed.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    accept_socket_connection()