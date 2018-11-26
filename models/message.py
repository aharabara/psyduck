from orator import Model, scope
from orator.orm import belongs_to


class Message(Model):

    __fillable__ = ['was_sent', 'content', 'receiver_id', 'sender_id']

    def __str__(self) -> str:
        # @todo display text for different users on different sides of textarea
        return self.sender.nickname + " >> " + self.content

    @belongs_to('sender_id')
    def sender(self):
        from models.user import User
        return User

    @belongs_to('receiver_id')
    def receiver(self):
        from models.user import User
        return User

    def to_dict(self):
        return {
            'content': self.content,
            'created_at': self.created_at,
        }
