import npyscreen
from psy.client.config import bus
from psy.forms.main_form import MainForm


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
