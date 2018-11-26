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

        user_a_id: int = query_builder.insert_get_id({
            'name': 'Alex', 'nickname': 'clientA', 'role_id': 1, 'key': 'pool-a'
        })
        user_b_id: int = query_builder.insert_get_id({
            'name': 'Alex', 'nickname': 'clientB', 'role_id': 1, 'key': 'pool-a', 'user_id': user_a_id
        })

        query_builder.where('id', user_a_id).update({'user_id' : user_b_id})

        query_builder.insert({
            'name': 'UserA', 'user_id': user_a_id, 'nickname': 'user-a-1', 'role_id': 2, 'key': 'pool-b'
        })
        query_builder.insert({
            'name': 'UserB', 'user_id': user_b_id, 'nickname': 'user-b', 'role_id': 2, 'key': 'pool-c'
        })
        pass

