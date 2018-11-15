from orator import Model
from orator.orm import has_one


class Message(Model):

    def __str__(self) -> str:
        return self.owner.nickname + " >> " + self.content

    @has_one
    def owner(self):
        from models.user import User
        return User
