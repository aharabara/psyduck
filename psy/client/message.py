from orator import Model

from psy.client.contact import Contact


class Message(Model):
    sender: Contact
    content: str
    was_sent: bool


    def __str__(self) -> str:
        return self.sender.nickname + " >> " + self.content
