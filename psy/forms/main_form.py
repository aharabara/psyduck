import curses
import logging
import sys

from threading import Thread
from typing import List, Optional, Dict

import npyscreen
from orator.support import Collection

from models.server import Server
from models.user import User
from psy import network
from psy.client import Client
from configs.config import bus

from models.message import Message
from psy.client.ui import Contacts, MessagesHistory, MessageBox


class MainForm(npyscreen.FormBaseNew):
    # UI
    messages_history: MessagesHistory
    message_box: MessageBox
    contacts_box: Contacts

    # User related entities
    user: User
    current_contact: User
    current_pool: Thread

    clients: Dict[str, Client]
    main_server: Server

    # Конструктор
    def create(self):
        # @todo add option parser
        self.user = User.query()\
            .where_has('role', lambda q: q.where('alias', '=', 'user'))\
            .where('nickname', sys.argv[1]).first()

        self.current_contact = self.user

        self.main_server = Server.query().where('alias', 'main').first()
        self.clients = dict()

        print(self.user)
        y, x = self.useable_space()

        # Добавляем виджет TitleText на форму
        self.contacts_box: Contacts = self.add(Contacts, name="Contacts", values=self.user.contacts, width=x // 4 - 4)
        self.messages_history: MessagesHistory = self.add(MessagesHistory, name="Chat", values=[], editable=False,
                                                          relx=x // 4, rely=2,
                                                          max_height=y // 4 * 3, max_width=x // 4 * 3)
        self.message_box = self.add(MessageBox, name="Message", value="", relx=x // 4, max_width=x // 4 * 3)

        self.setup_keyboard_handlers()

        self.contacts_box.value_changed_callback = self.on_contact_selection

        @bus.on('client:connection:status_changed')
        def connection_status_change(message: str):
            self.messages_history.name = message
            self.display()

        @bus.on('client:messages:sent')
        @bus.on('client:messages:received')
        def refresh(message: Message):
            self.display()

    @staticmethod
    def on_history_change(param):
        logging.info(param)

    def setup_keyboard_handlers(self):
        self.add_handlers({
            "^Q": self.quit,
        })
        self.message_box.add_handlers({
            curses.KEY_IC: self.send,
        })

    def on_contact_selection(self, widget):
        selected: List = self.contacts_box.get_value()
        if not len(selected):
            return

        current_contact = self.get_selected_contact()
        messages = self.get_dialog_messages()

        self.messages_history.values = messages

        client = self.clients.get(self.user.key)
        if not client:
            client = self.clients[self.user.key] = Client(self.main_server, self.user, current_contact,
                                                          self.messages_history.values)
            nat_type: Optional[str] = None
            try:
                nat_type = network.NATTYPE[int(sys.argv[4])]
            except IndexError:
                pass
            # todo
            # self.current_pool.STOP_OLD_THREAD()
            self.current_pool = Thread(target=client.main, args=[nat_type])
            self.current_pool.setDaemon(True)
            self.current_pool.start()
        self.display()

    def get_dialog_messages(self):
        return Message.query() \
            .where('sender_id', self.user.id).where('receiver_id', self.current_contact.id) \
            .or_where('receiver_id', self.user.id).where('sender_id', self.current_contact.id) \
            .get()

    def get_selected_contact(self):
        index: int = self.contacts_box.get_value().pop()
        self.current_contact = self.contacts_box.get_values()[index]
        return self.current_contact

    def quit(self, number):
        quit()

    def send(self, number):
        # self.user.messages.
        message = Message({
            'receiver_id': self.current_contact.id,
            'content': self.message_box.value,
            'was_sent': False,
        })
        self.current_contact.owned_messages().save(message)
        self.messages_history.values.append(message)
        self.message_box.value = ""
        bus.emit('client:messages:sent', message)
