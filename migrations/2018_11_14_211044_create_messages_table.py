from orator.migrations import Migration
from orator.schema import Blueprint


class CreateMessagesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """

        table: Blueprint

        with self.schema.create('messages') as table:
            table.increments('id')
            table.integer('sender_id')
            table.integer('receiver_id')
            table.boolean('was_sent')
            table.boolean('was_read').default(False)
            table.string('content')
            table.timestamps()

            table.foreign('receiver_id').references('id').on('users').on_delete('cascade')
            table.foreign('sender_id').references('id').on('users').on_delete('cascade')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('messages')
