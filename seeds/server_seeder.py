from orator import DatabaseManager
from orator.query import QueryBuilder
from orator.seeds import Seeder


class ServerSeeder(Seeder):

    def run(self):
        """
              Run the database seeds.
              """
        db: DatabaseManager = self.db
        query_builder: QueryBuilder = db.table('servers')

        query_builder.insert({
            'name': 'Main server', 'alias': 'main', 'ip': '127.0.0.1', 'port': 5678
        })

