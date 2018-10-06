#!/usr/bin/env python
# coding:utf-8
import socket
import sys
import time
from threading import Event, Thread

from psy import network


class Client():
    def __init__(self, master_ip, port, pool):
        try:
            self.master = (master_ip, int(port))
            self.pool = pool.strip()
            self.sockfd = self.target = None
            self.periodic_running = False
            self.peer_nat_type = None
        except (IndexError, ValueError):
            print(sys.stderr, "usage: %s <host> <port> <pool>" % sys.argv[0])
            sys.exit(65)

    def request_for_connection(self, nat_type_id=0):
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockfd.sendto(bytes(self.pool + ' {0}'.format(nat_type_id), 'utf-8'), self.master)
        data, addr = self.sockfd.recvfrom(len(self.pool) + 3)
        data = data.decode('utf-8')
        if data != "ok " + self.pool:
            print(sys.stderr, "unable to request!")
            sys.exit(1)
        self.sockfd.sendto(bytes("ok", 'utf-8'), self.master)
        sys.stderr = sys.stdout
        print(sys.stderr,
              "request sent, waiting for partner in pool '%s'..." % self.pool)
        data, addr = self.sockfd.recvfrom(8)

        self.target, peer_nat_type_id = network.bytes2addr(data)
        print(self.target, peer_nat_type_id)
        self.peer_nat_type = network.NATTYPE[peer_nat_type_id]
        print(sys.stderr, "connected to {1}:{2}, its NAT type is {0}".format(
            self.peer_nat_type, *self.target))

    def recv_msg(self, sock, is_restrict=False, event=None):
        if is_restrict:
            while True:
                data, addr = sock.recvfrom(1024)
                if self.periodic_running:
                    print("periodic_send is alive")
                    self.periodic_running = False
                    event.set()
                    print("received msg from target,"
                          "periodic send cancelled, chat start.")
                if addr == self.target or addr == self.master:
                    sys.stdout.write(data.decode('utf-8'))
                    if data == "punching...\n":
                        sock.sendto("end punching\n", addr)
        else:
            while True:
                data, addr = sock.recvfrom(1024)
                if addr == self.target or addr == self.master:
                    sys.stdout.write(data.decode('utf-8'))
                    if data == "punching...\n":  # peer是restrict
                        sock.sendto("end punching", addr)

    def send_msg(self, sock, message: str = None):
        while True:
            if message:
                sock.sendto(bytes(message, 'utf-8'), self.target)
            else:
                sock.sendto(bytes(sys.stdin.readline(), 'utf-8'), self.target)

    @staticmethod
    def start_working_threads(send, recv, event=None, *args, **kwargs):
        ts = Thread(target=send, args=args, kwargs=kwargs)
        ts.setDaemon(True)
        ts.start()
        if event:
            event.wait()
        tr = Thread(target=recv, args=args, kwargs=kwargs)
        tr.setDaemon(True)
        tr.start()

    def chat_fullcone(self):
        self.start_working_threads(self.send_msg, self.recv_msg, None,
                                   self.sockfd)

    def chat_restrict(self):
        from threading import Timer
        cancel_event = Event()

        def send(count):
            self.sockfd.sendto(bytes('punching...\n', 'utf-8'), self.target)
            print("UDP punching package {0} sent".format(count))
            if self.periodic_running:
                Timer(0.5, send, args=(count + 1,)).start()

        self.periodic_running = True
        send(0)
        kwargs = {'is_restrict': True, 'event': cancel_event}
        self.start_working_threads(self.send_msg, self.recv_msg, cancel_event,
                                   self.sockfd, **kwargs)

    def chat_symmetric(self):
        """
        Completely rely on relay server(TURN)
        """

        def send_msg_symm(sock):
            while True:
                data = 'msg ' + sys.stdin.readline()
                sock.sendto(bytes(data, 'utf-8'), self.master)

        def recv_msg_symm(sock):
            while True:
                data, addr = sock.recvfrom(1024)
                if addr == self.master:
                    sys.stdout.write(data.decode('utf-8'))

        self.start_working_threads(send_msg_symm, recv_msg_symm, None,
                                   self.sockfd)

    def main(self, test_nat_type=None):
        """
        nat_type是自己的nat类型
        peer_nat_type是从服务器获取的对方的nat类型
        选择哪种chat模式是根据nat_type来选择, 例如我这边的NAT设备是restrict, 那么我必须得一直向对方发包,
        我的NAT设备才能识别对方为"我已经发过包的地址". 直到收到对方的包, periodic发送停止
        """
        if not test_nat_type:
            nat_type, _, _ = network.get_nat_type()
        else:
            nat_type = test_nat_type  # 假装正在测试某种类型的NAT

        try:
            self.request_for_connection(nat_type_id=network.NATTYPE.index(nat_type))
        except ValueError:
            print("NAT type is %s" % nat_type)
            self.request_for_connection(nat_type_id=4)  # Unknown NAT

        if nat_type == network.UnknownNAT or self.peer_nat_type == network.UnknownNAT:
            print("Symmetric chat mode")
            self.chat_symmetric()
        if nat_type == network.SymmetricNAT or self.peer_nat_type == network.SymmetricNAT:
            print("Symmetric chat mode")
            self.chat_symmetric()
        elif nat_type == network.FullCone:
            print("FullCone chat mode")
            self.chat_fullcone()
        elif nat_type in (network.RestrictNAT, network.RestrictPortNAT):
            print("Restrict chat mode")
            self.chat_restrict()
        else:
            print("NAT type wrong!")

        while True:
            try:
                time.sleep(0.5)
            except KeyboardInterrupt:
                print("exit")
                sys.exit(0)
