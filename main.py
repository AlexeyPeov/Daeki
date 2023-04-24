import kivy

from kivy.app import App
from kivy.uix.label import Label

kivy.require('1.9.0')


class Aboba(App):

    def build(self):
        return Label(text="Aboba")


aboba = Aboba()
aboba.run()
