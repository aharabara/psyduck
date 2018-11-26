from typing import List

from orator import Model
from orator.orm import has_many, belongs_to
from models.role import Role


class User(Model):
    from models.message import Message

    name: str
    nickname: str
    key: str
    contacts: List[Message]

    @has_many
    def contacts(self):
        return User

    @has_many('sender_id')
    def owned_messages(self):
        from models.message import Message
        return Message

    @has_many('receiver_id')
    def received_messages(self):
        from models.message import Message
        return Message

    @belongs_to
    def role(self):
        return Role

    def __str__(self):
        return '@'+self.nickname
