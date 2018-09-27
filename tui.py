import curses

import npyscreen


class App(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="PsyDuck!")


class MessagesHistory(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Pager

class Contacts(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Pager


class MessageBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineEdit


class MainForm(npyscreen.FormBaseNew):

    input_box = None
    history = None
    contacts = None
    nickname = "aharabara"

    # Конструктор
    def create(self):
        y, x = self.useable_space()
        # Добавляем виджет TitleText на форму
        # self.contacts = self.add(Contacts, name="Contacts", values=["User1"], max_width=x // 10)
        self.history = self.add(MessagesHistory, name="Chat", values=["Messages"],
                                relx=x // 4, max_height=y // 4 * 3,
                                max_width=x // 4 * 3)
        self.input_box = self.add(MessageBox, name="Message", value="Hello World!",
                                  relx=x // 4, max_width=x // 4 * 3)

        self.add_handlers({
            "^Q": self.quit,
        })
        self.input_box.add_handlers({
            curses.KEY_IC: self.send,
        })

    def quit(self, number):
        quit()

    def send(self, number):
        self.history.values.append(self.nickname + " >> " + self.input_box.value)
        self.history.display()

        self.input_box.value = ""
        self.input_box.display()

    # # переопределенный метод, срабатывающий при нажатии на кнопку «ok»
    # def on_ok(self):
    #     self.parentApp.setNextForm(None)
    #
    # # переопределенный метод, срабатывающий при нажатии на кнопку «cancel»
    # def on_cancel(self):
    #     self.title.value = "Hello World!"


App().run()
