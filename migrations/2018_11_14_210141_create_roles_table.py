from orator.migrations import Migration
from orator.schema import Blueprint


class CreateRolesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        table: Blueprint
        with self.schema.create('roles') as table:
            table.increments('id')
            table.string('name')
            table.string('alias')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('roles')
