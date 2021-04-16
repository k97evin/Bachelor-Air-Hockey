#import kivy
import threading
import time
from kivy.app import App

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from kivy.properties import NumericProperty

from kivy.uix.popup import Popup
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.write()


#class Widgets(Widget):
#    def btn(self):
#       show_popup()





class Widget(Widget):
    score = NumericProperty(0)


class MainWindow(Screen):
    pass

class PlayGameWindow(Screen):
    pass

class LiveCalculationWindow(Screen):
    pass

class CameraWindow(Screen):
    pass

class CalibrationWindow(Screen):
    pass

class SettingsWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")


sm = WindowManager()

screens = [MainWindow(name="Main"),PlayGameWindow(name="Play_game"),LiveCalculationWindow(name="Live_calculation"),
            CameraWindow(name="Camera"),CalibrationWindow(name="Calibration"),SettingsWindow(name="Settings")]

for screen in screens:
    sm.add_widget(screen)


sm.current = "Main"

class MyApp(App):
    def build(self):
        return sm


def run():
    if __name__ == "__main__":
        MyApp().run()

#x = threading.Thread(target=run)

#x.start()

if __name__ == "__main__":
    MyApp().run()
