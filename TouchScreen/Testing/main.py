#import kivy
import threading
import time
from kivy.app import App

import cv2
import numpy as np

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import NumericProperty

from kivy.uix.popup import Popup
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.write()


#class Widgets(Widget):
#    def btn(self):
#       show_popup()





#class Widget(Widget):
#    score = NumericProperty(0)


class MainWindow(Screen):
    pass

class PlayGameWindow(Screen):
    pass

class LiveCalculationWindow(Screen):
    pass

class CameraWindow(Screen):

    font_size = NumericProperty(15)

    def slide_hue_min(self, *args):
        print(args[1])
        self.slide_text_hue_min.text = "Hue min: 0" + str(int(args[1]))
        #self.slide_text.font_size = str(int(args[1]) + 20)

    def slide_hue_max(self, *args):
        print(args[1])
        self.slide_text_hue_max.text = "Hue max: 0" + str(int(args[1]))

    def slide_sat_min(self, *args):
        print(args[1])
        self.slide_text_sat_min.text = "Sat min: 0" + str(int(args[1]))

    def slide_sat_max(self, *args):
        print(args[1])
        self.slide_text_sat_max.text = "Sat max: 0" + str(int(args[1]))

    def slide_val_min(self, *args):
        print(args[1])
        self.slide_text_val_min.text = "Val min: 0" + str(int(args[1]))

    def slide_val_max(self, *args):
        print(args[1])
        self.slide_text_val_max.text = "Val max: 0" + str(int(args[1]))

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
