from orator import Model
from orator.orm import has_many


class Role(Model):
    name: str
    alias: str

    @has_many
    def users(self):
        from models.user import User
        return User
