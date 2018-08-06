from queue import Queue, Empty
from threading import Thread
from random import randint

from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics import Rectangle

from motionize.ball_detection import run

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')

miner_position = Queue()


class MainScreen(FloatLayout):
    def __init__(self):
        open_cv = Thread(target=self.open_cv_worker, daemon=True)
        open_cv.start()
        super(MainScreen, self).__init__()
        self.points = 0
        self.score = Button(size_hint=(None, None), pos=(10, 10), size=(150, 40))
        self.score.text = 'Your Score is: {}'.format(self.points)
        self.add_widget(self.score)
        self.size_hint = None, None
        self.size = Config.get('graphics', 'width'), Config.get('graphics', 'height')
        with self.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos, source='assets/bg1.jpg')
        self.bounty = Image(source='assets/coin.jpg', size_hint=(None, None), size=(50, 50))
        self.dynamites = [
            Image(source='assets/dynamite.jpg', size_hint=(None, None), size=(30, 30)),
            Image(source='assets/dynamite.jpg', size_hint=(None, None), size=(30, 30)),
            Image(source='assets/dynamite.jpg', size_hint=(None, None), size=(30, 30)),
            Image(source='assets/dynamite.jpg', size_hint=(None, None), size=(30, 30)),
            Image(source='assets/dynamite.jpg', size_hint=(None, None), size=(30, 30)),
            Image(source='assets/dynamite.jpg', size_hint=(None, None), size=(30, 30)),
            Image(source='assets/dynamite.jpg', size_hint=(None, None), size=(30, 30))
        ]
        self.miner = Image(source='assets/miner.jpg', size_hint=(None, None), size=(50, 70))
        self.add_widget(self.miner)

        Clock.schedule_interval(self.update_miner_position, 0.1)
        Clock.schedule_interval(self.check_for_collision, 0.1)
        Clock.schedule_interval(self.manage_objects, 5)

    def open_cv_worker(self):
        run(miner_position)

    def check_for_collision(self, *args):
        if self.miner.collide_widget(self.bounty):
            self.remove_objects()
            self.points += 1
            self.score.text = 'Your Score is: {}'.format(self.points)
        else:
            for d in self.dynamites:
                if self.miner.collide_widget(d):
                    popup = Popup(
                        title='Ops!',
                        content=Label(text='You Lost! \n Score: {}'.format(self.points)),
                        auto_dismiss=False,

                        size_hint=(None, None),
                        size=(250, 250)
                    )
                    popup.open()

    def update_miner_position(self, *args):
        try:
            position = miner_position.get()
        except Empty:
            return
        self.miner.pos = position

    def manage_objects(self, *args):
        width = randint(0, Config.get('graphics', 'width'))
        height = randint(0, Config.get('graphics', 'height'))
        self.bounty.pos = width, height
        self.add_widget(self.bounty)
        for d in self.dynamites:
            width = randint(0, Config.get('graphics', 'width'))
            height = randint(0, Config.get('graphics', 'height'))
            d.pos = width, height
            self.add_widget(d)
        Clock.schedule_once(self.remove_objects, 3)

    def remove_objects(self, *args):
        self.remove_widget(self.bounty)
        self.bounty.pos = 100000, 100000
        for d in self.dynamites:
            self.remove_widget(d)
            d.pos = 100000, 100000


class Motionize(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    Motionize().run()
