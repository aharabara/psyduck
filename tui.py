import npyscreen

from psy.client.ui import QLTheme
from psy.forms.main_form import MainForm


class App(npyscreen.StandardApp):
    form: MainForm

    def main(self):
        npyscreen.setTheme(QLTheme)
        super().main()

    def onStart(self):
        self.form = self.addForm("MAIN", MainForm, name="PsyDuck!")

App().run()
