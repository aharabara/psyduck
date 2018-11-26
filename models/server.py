from typing import Tuple

from orator import Model


class Server(Model):
    name: str
    alias: str
    ip: str
    port: int

    def to_tuple(self) -> Tuple[str, int]:
        return self.ip, self.port
