import curses
import npyscreen

from typing import List
from psy.client import Contact
from psy.client.User import User
from psy.client.ui import Contacts, MessagesHistory, MessageBox


class App(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="PsyDuck!")


class MainForm(npyscreen.FormBaseNew):
    # UI
    messages_history: MessagesHistory
    message_box: MessageBox
    contacts_box: Contacts

    # User related entities
    user: User
    current_contact: Contact

    # Конструктор
    def create(self):
        self.user = User("Alexander", "aharabara", 0)
        self.current_contact = self.user

        y, x = self.useable_space()

        # Добавляем виджет TitleText на форму
        self.contacts_box = self.add(Contacts, name="Contacts", values=self.user.contact_list, width=x // 4 - 4)
        self.messages_history = self.add(MessagesHistory, name="Chat", values=["Messages"], editable=False,
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
            self.messages_history.display()

    def quit(self, number):
        quit()

    def send(self, number):
        self.messages_history.values.append(self.user.nickname + " >> " + self.message_box.value)
        self.messages_history.display()

        self.message_box.value = ""
        self.message_box.display()
        # self.client.send_msg(self.history.values)

    # # переопределенный метод, срабатывающий при нажатии на кнопку «ok»
    # def on_ok(self):
    #     self.parentApp.setNextForm(None)
    #
    # # переопределенный метод, срабатывающий при нажатии на кнопку «cancel»
    # def on_cancel(self):
    #     self.title.value = "Hello World!"


App().run()
#
# async def hello(name, timeout):
#     cnt = 0
#     while True and cnt < 5:
#         await asyncio.sleep(timeout)
#         print("Hello, {}".format(name))
#         cnt += 1
#
# if __name__ == '__main__':
#
#     tasks = [
#         hello("friends", 0.5),
#         hello("neighbours", 0.3),
#     ]
#
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asyncio.wait(tasks))
#     loop.close()
