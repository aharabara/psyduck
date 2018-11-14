from orator.migrations import Migration
from orator.schema import Blueprint

from models.user import User


class CreateUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """

        table: Blueprint = self.schema.create('users')
        table.increments('id')
        table.string('name')
        table.string('nickname')
        table.enum('role', [User.ROLE_USER, User.ROLE_CONTACT])
        table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('users')
