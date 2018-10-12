from typing import List

from psy.client import Contact


# Single instance
class User(Contact):
    contact_list: List = [
        Contact(name="Me", nickname="@room-one", pool=1),
        Contact(name="Ivan", nickname="@room-two", pool=2),
        Contact(name="Andrew", nickname="@room-three", pool=3),
    ]
