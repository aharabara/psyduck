import socket
import struct
import sys
from collections import namedtuple

NATTYPE = ('Full Cone', 'Restrict NAT', 'Restrict Port NAT', 'Symmetric NAT', 'Unknown NAT')

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



def main():
    port = int(sys.argv[1])
    # https://docs.python.org/3.6/library/socket.html
    sock_handle = socket.socket(type=socket.SOCK_DGRAM)
    sock_handle.bind(("", port))
    print("listening on *:%d (udp)" % port)
    poolqueue = {}
    symmetric_chat_clients = {}
    ClientInfo = namedtuple('ClientInfo', ['addr', 'nat_type_id'])

    while True:
        data, addr = sock_handle.recvfrom(1024)
        data = data.decode("utf-8")
        if data.startswith("msg ") and not symmetric_chat_clients: # ...and dict is not empty
            forward_msg(sock_handle, symmetric_chat_clients, data, addr)
        else:
            # help build connection between clients, act as STUN server
            print("connection from %s:%d" % addr)
            pool, nat_type_id = data.strip().split()
            sock_handle.sendto(bytes("ok {0}".format(pool), 'utf-8'), addr)
            print("pool={0}, nat_type={1}, ok sent to client".format(pool, NATTYPE[int(nat_type_id)]))
            data, addr = sock_handle.recvfrom(2)
            data = data.decode('utf-8')
            if data != "ok":
                continue

            print("request received for pool:", pool)

            try:
                a, b = poolqueue[pool].addr, addr
                nat_type_id_a, nat_type_id_b = poolqueue[pool].nat_type_id, nat_type_id
                sock_handle.sendto(addr2bytes(a, nat_type_id_a), b)
                sock_handle.sendto(addr2bytes(b, nat_type_id_b), a)
                print("linked", pool)
                del poolqueue[pool]
            except KeyError:
                poolqueue[pool] = ClientInfo(addr, nat_type_id)

            if pool in symmetric_chat_clients:
                if nat_type_id == '3' or symmetric_chat_clients[pool][0] == '3':
                    # at least one is symmetric NAT
                    recorded_client_addr = symmetric_chat_clients[pool][1]
                    symmetric_chat_clients[addr] = recorded_client_addr
                    symmetric_chat_clients[recorded_client_addr] = addr
                    print("Hurray! symmetric chat link established.")
                    del symmetric_chat_clients[pool]
                else:
                    del symmetric_chat_clients[pool]  # neither clients are symmetric NAT
            else:
                symmetric_chat_clients[pool] = (nat_type_id, addr)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: server.py port")
        exit(0)
    assert sys.argv[1].isdigit(), "port should be a number!"
    main()
