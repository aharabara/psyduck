from typing import List

from psy.client import Contact


# Single instance
class User(Contact):
    contact_list: List = [
        Contact(name="Me", nickname="@user", pool=1),
        Contact(name="Ivan", nickname="@ivan", pool=2),
        Contact(name="Andrew", nickname="@andrew", pool=3),
    ]
