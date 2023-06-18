import random

from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.image import Image, AsyncImage
from kivymd.app import MDApp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import ObjectProperty, ColorProperty
from kivy.uix.label import Label
from kivy.config import Config
import os

import movie_finder


# Set the window to not be resizable
Config.set('graphics', 'resizable', 0)
Config.set('kivy', 'window', 'sdl2')

# Set the window size
Window.size = (600, 819)

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
        base = movie_finder.read_from_file('liked.txt')
        layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter("height"))

        def on_button_release(button):
            index = layout.children.index(button)

            movie_to_remove = layout.children[index + 1].text


            # Read the movies from the movies.txt file into a list
            with open('liked.txt', 'r', encoding='utf-8') as f:
                movies = [line.strip() for line in f]

            # Remove the desired movie from the list
            if movie_to_remove in movies:
                movies.remove(movie_to_remove)

            # Write the updated list of movies back to the movies.txt file
            with open('liked.txt', 'w', encoding='utf-8') as f:
                for movie in movies:
                    f.write(movie + '\n')

            # Append the removed movie to the watched.txt file
            with open('exceptions.txt', 'a', encoding='utf-8') as f:
                f.write(movie_to_remove + '\n')

            layout.remove_widget(button)
            layout.remove_widget(layout.children[index])


        for element in base:
            label = Label(text=element, size=(50, 50), halign='left', text_size=(230, None), size_hint=(1, None))
            button = Button(text="X", size=(50, 50), size_hint=(0.15, None),
                            background_color=(0.5, 0.5, 0.5, 0), color=(1, 0, 0, 1),
                            on_release=on_button_release)
            layout.add_widget(label)
            layout.add_widget(button)

        scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scrollview.add_widget(layout)
        self.view.add_widget(scrollview)


class Options(FloatLayout):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


#
# Label:
# id: rating_text
# bold: True
# text: app.get_rating()
# pos: root.width / 2.85, root.y + 30

class MyApp(MDApp):
    def build(self):
        self.project_dir = os.getcwd()
        self.rating = round(random.uniform(1, 10), 1)

        self.exeptions, self.liked_movies = movie_finder.init_movie_finder()
        movie_data = movie_finder.get_movie(self.rating,
                                            self.rating,
                                            self.exeptions,
                                            self.liked_movies)

        while(not movie_data):
            self.rating = round(random.uniform(1, 10), 1)
            movie_data = movie_finder.get_movie(self.rating,
                                                self.rating,
                                                self.exeptions,
                                                self.liked_movies)

        movie_id, self.movie_title, self.movie_overview, movie_rating, poster_path = movie_data

        base_url = "https://image.tmdb.org/t/p/w500"
        self.poster_url = base_url + poster_path if poster_path else "https://via.placeholder.com/500x750.png?text=No+poster+available"

        self.grid = MyGrid()

        img = self.grid.ids.bg_image
        box_1 = self.grid.ids.box_1

        self.movie_title_text = Label(bold=True, text=self.movie_title, pos=(250,650), pos_hint={"center_x": 0.5, "center_y": 0.5})

        img.source = self.poster_url
        img.size_hint = (0.1, 0.055)

        layout = self.grid.ids.float_layout
        main_box = self.grid.ids.main_box
        slider_layout = self.grid.ids.slider_box

        self.label = Label(bold=True, text=f'Rating: {self.rating}', pos_hint={"center_x": 0.5, "center_y": 0.5})

        self.movie_description = Label(bold=True, text=self.movie_overview, text_size=(270, None), halign='left',
                                       pos = (400, 450))

        self.slider = Slider(min=1.1, max=10, step=0.1)
        self.slider.value = self.rating
        self.slider.bind(value=self.on_value)

        self.slider.pos = slider_layout.pos

        slider_layout.add_widget(self.slider)

        layout.add_widget(self.label)
        main_box.add_widget(self.movie_title_text)
        main_box.add_widget(self.movie_description)

        return self.grid

    def on_value(self, instance, value):
        self.rating = round(value, 1)
        self.label.text = f'{self.rating} / 10'

    def get_rating(self):
        return f'{self.rating} / 10'

    def get_movie(self):
        movie_data = movie_finder.get_movie(self.rating,
                                            self.rating,
                                            self.exeptions,
                                            self.liked_movies)

        if (not movie_data): return

        movie_id, self.movie_title, self.movie_overview, movie_rating, poster_path = movie_data
        base_url = "https://image.tmdb.org/t/p/w500"
        self.poster_url = base_url + poster_path if poster_path else "https://via.placeholder.com/500x750.png?text=No+poster+available"

        img = self.grid.ids.bg_image

        img.source = self.poster_url

        self.movie_description.text = self.movie_overview
        self.movie_title_text.text = self.movie_title

    def liked(self):
        if (self.movie_title):
            movie_finder.write_to_file("liked.txt", self.movie_title)
            self.liked_movies.append(self.movie_title)  # Добавляем фильм в список понравившихся
            self.movie_title = ""

    def disliked(self):
        if (self.movie_title):
            movie_finder.write_to_file("exceptions.txt", self.movie_title)
            self.exeptions.append(self.movie_title)
            self.movie_title = ""


def show_popup1():
    show = Favorite()

    popupWindow = Popup(title="Посмотреть потом", content=show, size_hint=(None, None), size=(300, 500),
                        background='Dark', background_color='#744d4d')

    popupWindow.open()


def show_popup2():
    show = Options()

    popupWindow = Popup(title="Настройки", content=show, size_hint=(None, None), size=(300, 500), background='Dark',
                        background_color='#744d4d')

    popupWindow.open()


if __name__ == "__main__":
    MyApp().run()

