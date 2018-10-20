import npyscreen


class MessagesHistory(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Pager


class Contacts(npyscreen.BoxTitle):
    _contained_widget = npyscreen.SelectOne


class MessageBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineEdit
