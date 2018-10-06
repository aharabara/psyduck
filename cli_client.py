import sys

from psy import network
from psy.client import Client

if __name__ == "__main__":
    try:
        master_ip = '127.0.0.1' if sys.argv[1] == 'localhost' else sys.argv[1]
        client = Client(master_ip, sys.argv[2], sys.argv[3])

        try:
            test_nat_type = network.NATTYPE[int(sys.argv[4])]
        except IndexError:
            test_nat_type = None

        client.main(test_nat_type)
    except (IndexError, ValueError):
        print(sys.stderr, "usage: %s <host> <port> <pool>" % sys.argv[0])
        sys.exit(65)