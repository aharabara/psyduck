import sys

from typing import Optional
from psy import network
from psy.client import Client

if __name__ == "__main__":
    try:
        master_ip: str = '127.0.0.1' if sys.argv[1] == 'localhost' else sys.argv[1]
        port: int = int(sys.argv[2].strip())
        pool: str = sys.argv[3]

        client: Client = Client(master_ip, port, pool)
        nat_type: Optional[str] = None
        try:
            nat_type = network.NATTYPE[int(sys.argv[4])]
        except IndexError:
            pass

        client.main(nat_type)
    except (IndexError, ValueError):
        print(sys.stderr, "usage: %s <host> <port> <pool>" % sys.argv[0])
        sys.exit(65)
