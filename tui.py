import curses

import npyscreen

from psy_net import nat_utils
from client.client import Client
from client.contact import Contact


class App(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="PsyDuck!")


class MessagesHistory(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Pager


class Contacts(npyscreen.BoxTitle):
    _contained_widget = npyscreen.SelectOne


class MessageBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineEdit


class MainForm(npyscreen.FormBaseNew):
    input_box = None
    history = None
    contacts = None
    nickname = "aharabara"
    # switch from dict to Contact entity.
    contacts_list = [
        Contact(name="Me", nickname="@user", pool=1),
        Contact(name="Ivan", nickname="@ivan", pool=2),
        Contact(name="Andrew", nickname="@andrew", pool=3),
    ]

    # Конструктор
    def create(self):
        y, x = self.useable_space()
        # Добавляем виджет TitleText на форму
        self.contacts = self.add(Contacts, name="Contacts", values=self.contacts_list, width=x // 4 - 4)
        self.history = self.add(MessagesHistory, name="Chat", values=["Messages"], editable=False,
                                relx=x // 4,
                                rely=2,
                                max_height=y // 4 * 3,
                                max_width=x // 4 * 3)
        self.input_box = self.add(MessageBox, name="Message", value="Hello World!", relx=x // 4, max_width=x // 4 * 3)

        self.add_handlers({
            "^Q": self.quit,
        })
        self.input_box.add_handlers({
            curses.KEY_IC: self.send,
        })

        self.contacts.value_changed_callback = self.select_pool

        # master_ip = '127.0.0.1' if sys.argv[1] == 'localhost' else sys.argv[1]
        # client = Client("localhost", "5678", "1")
        #
        # test_nat_type = nat_utils.NATTYPE[0]  # 输入数字0,1,2,3
        #
        # client.main(test_nat_type)

    def select_pool(self, widget):
        selected = list(self.contacts.get_value())
        print(selected.pop())
        if selected.count(selected):
            index = self.contacts.get_value().pop()
            print(self.contacts.get_values()[index])

    def quit(self, number):
        quit()

    def send(self, number):
        self.history.values.append(self.nickname + " >> " + self.input_box.value)
        self.history.display()

        self.input_box.value = ""
        self.input_box.display()
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