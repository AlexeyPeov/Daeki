from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
import os
from kivy.uix.effectwidget import EffectWidget
#from kivy_garden.frostedglass import FrostedGlass

import movie_finder

class MyGrid(Widget):
    def btn1(self):
        show_popup1()

    def btn2(self):
        show_popup2()

class MyBtns(GridLayout):
    pass

class Favorite(Screen):
    view = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Favorite, self).__init__(**kwargs)
        Clock.schedule_once(self.create_scrollview)

    def create_scrollview(self, dt):
        base = ["element {}".format(i) for i in range(20)]
        layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))

        for element in base:
            layout.add_widget(Label(text=element, size=(50, 50), size_hint=(1, None)))
            layout.add_widget(Button(text="X", size=(50, 50), size_hint=(0.15, None),
                                     background_color=(0.5, 0.5, 0.5, 0), color=(1, 0, 0, 1)))
        scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scrollview.add_widget(layout)
        self.view.add_widget(scrollview)

class Options(FloatLayout):
    pass

class ImageButton(ButtonBehavior, Image):
    pass

class MyApp(MDApp):
    def build(self):
        Window.clearcolor = '#FAEEE5'
        self.project_dir = os.getcwd()
        return MyGrid()

def show_popup1():
    show = Favorite()

    popupWindow = Popup(title="Посмотреть потом", content=show, size_hint=(None, None), size=(300,500), background='Dark', background_color='#744d4d')

    popupWindow.open()

def show_popup2():
    show = Options()

    popupWindow = Popup(title="Настройки", content=show, size_hint=(None, None), size=(300,500), background='Dark', background_color='#744d4d')

    popupWindow.open()

if __name__ == "__main__":
    MyApp().run()
