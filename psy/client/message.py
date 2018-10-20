from psy.client.contact import Contact


class Message:
    sender: Contact
    content: str
    was_sent: bool

    def __init__(self, sender: Contact, content: str) -> None:
        self.sender = sender
        self.content = content
        self.was_sent = False

    def __str__(self) -> str:
        return self.sender.nickname + " >> " + self.content
