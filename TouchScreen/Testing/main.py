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
    counter = NumericProperty(0)
    
    def Counter_function(self):
        self.counter += 1
        self.ids.lbl.text = "Tall: {}".format(self.counter)

    def First_thread(self):
        threading.Thread(target = self.Counter_function).start()

        self.counter += 1
        self.ids.lbl.text = "Tall: {}".format(self.counter)

    def test(self):
        threading.Thread(target= testenoe,args=[self],daemon=True).start()  #daemon gjør sånn at når main avslutter blir denne tråden drept
        #testenoe(self)

class LiveCalculationWindow(Screen):
    pass



class CameraWindow(Screen):

    font_size = NumericProperty(15)
    hue_min = 0
    hue_max = 0
    sat_min = 0
    sat_max = 0
    val_min = 0
    val_max = 0


    def slide_hue_min(self, *args):
        #print(int(args[1]))
        self.hue_min = int(args[1])
        self.slide_text_hue_min.text = "Hue min: " + str(self.hue_min)
        #print(str(self.hue_min))
        #self.slide_text.font_size = str(int(args[1]) + 20)

    def slide_hue_max(self, *args):
        self.hue_max = int(args[1])
        self.slide_text_hue_max.text = "Hue max: " + str(self.hue_max)

    def slide_sat_min(self, *args):
        self.sat_min = int(args[1])
        self.slide_text_sat_min.text = "Sat min: " + str(self.sat_min)

    def slide_sat_max(self, *args):
        self.sat_max = int(args[1])
        self.slide_text_sat_max.text = "Sat max: " + str(self.sat_max)

    def slide_val_min(self, *args):
        self.val_min = int(args[1])
        self.slide_text_val_min.text = "Val min: " + str(self.val_min)

    def slide_val_max(self, *args):
        self.val_max = int(args[1])
        self.slide_text_val_max.text = "Val max: " + str(self.val_max)


        #ColorPicker
    



class CalibrationWindow(Screen):
    pass

class SettingsWindow(Screen):
    pass

class WindowManager(ScreenManager):

    pass

kv = Builder.load_file("my.kv")

# OLD OLD OLD OLD
#sm = WindowManager()
#screens = [MainWindow(name="Main"),PlayGameWindow(name="Play_game"),LiveCalculationWindow(name="Live_calculation"),
#            CameraWindow(name="Camera"),CalibrationWindow(name="Calibration"),SettingsWindow(name="Settings")]
#for screen in screens:
#    sm.add_widget(screen)
#sm.current = "Main"
# OLD OLD OLD OLD

def testenoe(objekt):
    for _ in range (3):
        a = input("Test: ")
        objekt.counter = int(a)
        objekt.ids.lbl.text = "{}".format(objekt.counter)

    #for _ in range(5):
        #objekt.counter = int(input())
        #objekt.ids.lbl.text = "{}".format(objekt.counter)

class MyApp(App):
    def build(self):
        return kv


# OLD OLD OLD OLD
#def run():
 #   if __name__ == "__main__":
  #      MyApp().run()

#x = threading.Thread(target=run)
#x.start()
# OLD OLD OLD OLD

if __name__ == "__main__":
    MyApp().run()


