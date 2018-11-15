from orator import DatabaseManager
from orator.query import QueryBuilder
from orator.seeds import Seeder


class UsersSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        db: DatabaseManager = self.db
        query_builder: QueryBuilder = db.table('users')

        user_id: int = query_builder.insert_get_id({
            'name': 'Alex', 'nickname': 'Alex', 'role_id': 1, 'key': 'pool-a'
        })

        query_builder.insert({
            'name': 'UserA', 'user_id': user_id, 'nickname': 'user-a', 'role_id': 2, 'key': 'pool-b'
        })
        query_builder.insert({
            'name': 'UserB', 'user_id': user_id, 'nickname': 'user-b', 'role_id': 2, 'key': 'pool-c'
        })
        pass

