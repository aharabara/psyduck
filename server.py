import socket
import struct
import sys
import json
from collections import namedtuple

NATTYPE = ('Full Cone', 'Restrict NAT', 'Restrict Port NAT', 'Symmetric NAT', 'Unknown NAT')
'''
def addr2bytes(addr: tuple, nat_type_id: int):
    """Convert an address pair to a hash."""
    host, port = addr
    try:
        host = socket.gethostbyname(host)
    except (socket.gaierror, socket.error):
        raise ValueError("invalid host")
    try:
        port = int(port)
    except ValueError:
        raise ValueError("invalid port")
    try:
        nat_type_id = int(nat_type_id)
    except ValueError:
        raise ValueError("invalid NAT type")
    bytes = socket.inet_aton(host)
    bytes += struct.pack("H", port)
    bytes += struct.pack("H", nat_type_id)
    return bytes

# forward symmetric chat msg, act as TURN server
def forward_msg(sock_handle: socket, clients: dict, data, addr):
    try:
        sock_handle.sendto(bytes(data[4:], 'utf-8'), clients[addr])
        print("msg successfully forwarded to {0}".format(clients[addr]))
        print(data[4:]) # we should probably use some other clever way to do this
    except KeyError:
        print("something is wrong with symmetric_chat_clients!")
        print(clients[addr]) # for debugging purpose only
'''
def establish_connection(sock: socket, pool: int, nat_type_id: int, addr: tuple):
    print(addr)
    sock.sendto(bytes("ok {0}".format(pool), 'utf-8'), addr)
    print("pool={0}, nat_type={1}, ok sent to client".format(pool, NATTYPE[int(nat_type_id)]))
    data, addr = sock.recvfrom(2)
    data = data.decode('utf-8')
    print(data == "ok")
    return data == "ok"

def main():
    port = int(sys.argv[1])
    # https://docs.python.org/3.6/library/socket.html
    sock_handle = socket.socket(type=socket.SOCK_DGRAM)
    sock_handle.bind(('0.0.0.0', port))
    print("listening on *:%d (UDP)" % port)
    poolqueue = {}
    chat_clients = {}

    ClientInfo = namedtuple('ClientInfo', ['addr', 'nat_type_id'])

    # todo authentication with JWT ?
    while True:
        print(poolqueue)
        print(chat_clients)
        data, addr = sock_handle.recvfrom(1024)
        print("connection from %s:%d" % addr)

        if data == b'\n':
            print('data is empty')
            continue
        data = data.decode("utf-8")
        # how client knows about NAT type ? Network Address Translation
        if len(data.split()) < 2:
            print('not enough data')
            continue

        # help build connection between clients, act as STUN server
        pool, nat_type_id = data.strip().split()
        if not establish_connection(sock_handle, pool, nat_type_id, addr):
            print('connection is not okay')
            continue
        print("request received for pool:", pool)

        try:
            # here happens the actual exchange of client addresses
            # send each client the opposite address so they can talk without the server
            firstUser, secondUser = poolqueue[pool].addr, addr
            natFirstUser, natSecondUser = poolqueue[pool].nat_type_id, nat_type_id
            sock_handle.sendto(bytes(json.dumps(secondUser), 'utf-8'), firstUser)
            sock_handle.sendto(bytes(json.dumps(firstUser), 'utf-8'), secondUser)
            print("linked", pool)
            del poolqueue[pool]
        except KeyError:
            poolqueue[pool] = ClientInfo(addr, nat_type_id)

        if pool in chat_clients:
            if nat_type_id == '3' or chat_clients[pool][0] == '3':
                # at least one is symmetric NAT
                recorded_client_addr = chat_clients[pool][1]
                chat_clients[addr] = recorded_client_addr
                chat_clients[recorded_client_addr] = addr
                print("Hurray! symmetric chat link established.")
                del chat_clients[pool]
            else:
                del chat_clients[pool]  # neither clients are symmetric NAT
        else:
            chat_clients[pool] = (nat_type_id, addr)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: server.py port")
        exit(0)
    assert sys.argv[1].isdigit(), "port should be a number!"
    main()
