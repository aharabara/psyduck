import socket
import struct
import sys
import json

'''
usefull links:
https://docs.python.org/3.6/library/socket.html

'''

def validateData(data):
    try:
        dct = json.loads(data)
    except ValueError:
        return False
    if not isinstance(dct, dict) or 'login' not in dct:
        return False
    return True

def main():
    port = int(sys.argv[1])
    sock_handle = socket.socket(type=socket.SOCK_DGRAM)
    sock_handle.bind(('0.0.0.0', port))
    print("listening on *:%d (UDP)" % port)
    clients = []
    while True:
        print(clients)
        data, addr = sock_handle.recvfrom(1024)
        data = data.decode("utf-8")
        if not validateData(data):
            continue
        data = json.loads(data)
        data['addr'] = addr[0]
        data['port'] = addr[1]
        print(data)
        if data not in clients:
            clients.append(data)
        sock_handle.sendto(bytes(json.dumps(clients), 'utf-8'), (data['addr'], data['port']))
        continue

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: server.py port")
        exit(0)
    assert sys.argv[1].isdigit(), "port should be a number!"
    main()
