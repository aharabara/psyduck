import curses
import sys
import npyscreen

from threading import Thread
from typing import List, Optional

from psy import network
from psy.client import Client, Contact
from psy.client.config import bus

from psy.client.user import User
from psy.client.message import Message
from psy.client.ui import Contacts, MessagesHistory, MessageBox


class MainForm(npyscreen.FormBaseNew):
    # UI
    messages_history: MessagesHistory
    message_box: MessageBox
    contacts_box: Contacts

    # User related entities
    user: User
    current_contact: Contact
    current_pool: Thread

    # Конструктор
    def create(self):
        self.user = User("Alexander", "aharabara", 0)
        self.current_contact = self.user

        y, x = self.useable_space()

        # Добавляем виджет TitleText на форму
        self.contacts_box = self.add(Contacts, name="Contacts", values=self.user.contact_list, width=x // 4 - 4)
        self.messages_history = self.add(MessagesHistory, name="Chat", values=[], editable=False,
                                         relx=x // 4, rely=2,
                                         max_height=y // 4 * 3, max_width=x // 4 * 3)

        self.message_box = self.add(MessageBox, name="Message", value="Hello World!", relx=x // 4, max_width=x // 4 * 3)

        self.setup_keyboard_handlers()

        self.contacts_box.value_changed_callback = self.select_contact

    def setup_keyboard_handlers(self):
        self.add_handlers({
            "^Q": self.quit,
        })
        self.message_box.add_handlers({
            curses.KEY_IC: self.send,
        })

    def select_contact(self, widget):
        selected: List = self.contacts_box.get_value()
        if len(selected):
            index: int = self.contacts_box.get_value().pop()
            self.current_contact = self.contacts_box.get_values()[index]
            self.messages_history.values = self.current_contact.messages
            master_ip: str = '127.0.0.1'
            port: int = 5678
            pool: str = str(self.current_contact.pool)

            client: Client = Client(master_ip, port, pool, self.current_contact.messages)
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

    def quit(self, number):
        quit()

    def send(self, number):
        message = Message(self.user, self.message_box.value)
        self.messages_history.values.append(message)
        self.message_box.value = ""
        bus.emit('client:messages:sent', message)


class App(npyscreen.StandardApp):
    form: MainForm

    def onStart(self):
        self.form = self.addForm("MAIN", MainForm, name="PsyDuck!")

    def refresh(self):
        self.form.messages_history.display()
        self.form.message_box.display()


app = App()


@bus.on('client:messages:sent')
@bus.on('client:messages:received')
def on_change(*args):
    app.refresh()


app.run()
