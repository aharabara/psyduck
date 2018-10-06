from typing import List


class Contact:
    messages: List
    nickname: str
    name: str
    pool: int

    def __init__(self, name: str, nickname: str, pool: int) -> None:
        self.messages = []
        self.nickname = nickname
        self.name = name
        self.pool = pool

    def __str__(self) -> str:
        return self.nickname

    def add_msg(self, message: str):
        self.messages.append(message)
