from queue import Queue, Empty
from threading import Thread
from random import randint

from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock

from motionize.HandRecognition import run

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

hand_position = Queue()


class MainScreen(FloatLayout):
    def __init__(self):
        open_cv = Thread(target=self.open_cv_worker, daemon=True)
        open_cv.start()
        super(MainScreen, self).__init__()
        self.bounty = Image(source='assets/coin.jpg', size_hint=(None, None), size=(40, 40))
        self.btn = Image(source='assets/miner.jpg', size_hint=(None, None), size=(50, 60))
        self.add_widget(self.btn)

        Clock.schedule_interval(self.update_hand_position, 0.1)
        Clock.schedule_interval(self.manage_bounty, 5)

    def open_cv_worker(self):
        run(hand_position)

    def update_hand_position(self, *args):
        try:
            position = hand_position.get()
        except Empty:
            return
        self.btn.pos = position

    def manage_bounty(self, *args):
        width = randint(0, 800)
        height = randint(0, 600)
        self.bounty.pos = width, height
        self.add_widget(self.bounty)
        Clock.schedule_once(self.remove_bounty, 3)

    def remove_bounty(self, *args):
        self.remove_widget(self.bounty)


class Motionize(App):
    def build(self):
        return MainScreen()


if __name__ == '__main__':
    Motionize().run()
