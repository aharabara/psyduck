from orator.seeds import Seeder

from seeds.users_seeder import UsersSeeder
from seeds.role_seeder import RoleSeeder


class DatabaseSeeder(Seeder):

    def run(self):
        """
        Run the database seeds.
        """
        self.call(RoleSeeder)
        self.call(UsersSeeder)
        pass

