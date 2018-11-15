from orator import DatabaseManager
from orator.query import QueryBuilder
from orator.seeds import Seeder


class RoleSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        db: DatabaseManager = self.db
        query_builder: QueryBuilder = db.table('roles')

        query_builder.insert({
            'name': 'User', 'alias': 'user'
        })

        query_builder.insert({
            'name': 'Contact', 'alias': 'contact'
        })


        pass

