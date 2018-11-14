from orator import Model
from orator.orm import has_many


class User(Model):
    ROLE_USER: str = 'ROLE_USER'
    ROLE_CONTACT: str = 'ROLE_CONTACT'

    @has_many
    def contacts(self):
        return User
