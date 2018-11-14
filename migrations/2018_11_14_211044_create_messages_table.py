from orator.migrations import Migration


class CreateMessagesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('messages') as table:
            table.increments('id')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('messages')
