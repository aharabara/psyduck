from orator.migrations import Migration
from orator.schema import Blueprint


class CreateUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """

        table: Blueprint
        with self.schema.create('users') as table:
            table.increments('id')
            table.string('name')
            table.string('nickname')
            table.text('key')
            table.integer('user_id').nullable()
            table.integer('role_id')
            table.timestamps()

            table.foreign('user_id').references('id').on('users').on_delete('cascade')
            table.foreign('role_id').references('id').on('roles').on_delete('cascade')


    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('users')
