import socket
import threading
import sys
import os

server_ip = '127.0.0.1'
server_port = 12347

name = sys.argv[1]
message_for_send = sys.argv[1]

def client_send_thread(tcp_connection):
    if len(sys.argv) < 3:
        print('no have message for send to the server')
        return None

    message = sys.argv[2]

    try:
        tcp_connection.send(str.encode(message))
    except Exception as ex:
        print('have exception when send message, ', ex)

def client_receive_thread(tcp_connection):
    global name

    handshake_message = f'handshake,{name}'
    tcp_connection.send(str.encode(handshake_message))

    while True:
        try:
            res = tcp_connection.recv(1024)
            recieved_data = str(res.decode('ascii'))
            print(recieved_data)
        except Exception as ex:
            print('have exception when recieve data from server err: ', ex)
            tcp_connection.close()

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((server_ip,server_port))

    threading.Thread(target=client_receive_thread, args=(client_socket, )).start()
    threading.Thread(target=client_send_thread, args=(client_socket, )).start()


if __name__ == '__main__':
    try:
        connect_to_server()
    except KeyboardInterrupt:
        print('client closed.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
        