from orator.migrations import Migration
from orator.schema import Blueprint


class CreateServersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        table: Blueprint
        with self.schema.create('servers') as table:
            table.increments('id')
            table.string('name')
            table.string('alias')
            table.string('ip')
            table.integer('port')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('servers')
