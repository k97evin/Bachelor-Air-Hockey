#import kivy
import threading
import time
from kivy.app import App

import cv2
from kivy.core import window
import numpy as np

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.popup import Popup

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
    #colorW = ObjectProperty()
    def QuitApp(self):
        App.get_running_app().stop()
        Window.close()
    
    # def GetColorsToColorWindow(self):
    #     self.manager.current = "ColorDetectionWindow"
    #     self.GetColors()

class PlayGameWindow(Screen):

    font_size_score = 125

    def ScorePlayer(self, increment):
        self.score_player = int(self.ids.score_player.text)
        if increment == 1:
            self.score_player += 1
        else:
            self.score_player -= 1
        if self.score_player <= 0:
            self.score_player = 0
        elif self.score_player >= 9:
            self.score_player = 9
        self.ids.score_player.text = "{}".format(self.score_player)

    def ScoreRobot(self, increment):
        self.score_robot = int(self.ids.score_robot.text)
        if increment == 1:
            self.score_robot += 1
        else:
            self.score_robot -= 1
        if self.score_robot <= 0:
            self.score_robot = 0
        elif self.score_robot >= 9:
            self.score_robot = 9
        self.ids.score_robot.text = "{}".format(self.score_robot)
    

class LiveCalculationWindow(Screen):
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
        



class ColorDetectionWindow(Screen):
    lock = threading.Lock()
    
    font_size = 15
    hue_min = 50
    hue_max = 170
    sat_min = 150
    sat_max = 255
    val_min = 0
    val_max = 255
    img_src = 'test.png'
    

    def GetColors(self):
        try:
            f = open('test_color.txt', 'r')
            data = []
            read = f.readline()
            doneReading = False

            while(not doneReading):
                data.append(read)
                read = f.readline()
                
                if "END" in read:
                    data.append(read)
                    f.close()
                    doneReading = True
                    break
            self.lock.acquire()
            for color in data:
                if 'LAST' in color:
                    self.last_col = color[color.find("LAST: ") + len("LAST: "): color.find(";")]
                    self.last_col_val = self.last_col.split(" ")
                    self.hue_min = int(self.last_col_val[0])
                    self.hue_max = int(self.last_col_val[1])
                    self.sat_min = int(self.last_col_val[2])
                    self.sat_max = int(self.last_col_val[3])
                    self.val_min = int(self.last_col_val[4])
                    self.val_max = int(self.last_col_val[5])

                    self.ids.hue_min_label.text = "Hue min: " + str(self.hue_min)
                    self.ids.hue_min_slider.value = self.hue_min
                    self.ids.hue_max_label.text = "Hue max: " + str(self.hue_max)
                    self.ids.hue_max_slider.value = self.hue_max

                    self.ids.sat_min_label.text = "Sat min: " + str(self.sat_min)
                    self.ids.sat_min_slider.value = self.sat_min
                    self.ids.sat_max_label.text = "Sat max: " + str(self.sat_max)
                    self.ids.sat_max_slider.value = self.sat_max  

                    self.ids.val_min_label.text = "val min: " + str(self.val_min)
                    self.ids.val_min_slider.value = self.val_min
                    self.ids.val_max_label.text = "val max: " + str(self.val_max)
                    self.ids.val_max_slider.value = self.val_max 

                if 'BLUE' in color:
                    self.blue_col = color[color.find("BLUE: ") + len("BLUE: "): color.find(";")]
                    blue_col_val = self.blue_col.split(" ")
                    self.hue_min_blue = int(blue_col_val[0])
                    self.hue_max_blue = int(blue_col_val[1])
                    self.sat_min_blue = int(blue_col_val[2])
                    self.sat_max_blue = int(blue_col_val[3])
                    self.val_min_blue = int(blue_col_val[4])
                    self.val_max_blue = int(blue_col_val[5])

                if 'YELLOW' in color:
                    self.yellow_col = color[color.find("YELLOW: ") + len("YELLOW: "): color.find(";")]
                    yellow_col_val = self.yellow_col.split(" ")
                    self.hue_min_yellow = int(yellow_col_val[0])
                    self.hue_max_yellow = int(yellow_col_val[1])
                    self.sat_min_yellow = int(yellow_col_val[2])
                    self.sat_max_yellow = int(yellow_col_val[3])
                    self.val_min_yellow = int(yellow_col_val[4])
                    self.val_max_yellow = int(yellow_col_val[5])

                if 'GREEN' in color:
                    self.green_col = color[color.find("GREEN: ") + len("GREEN: "): color.find(";")]
                    green_col_val = self.green_col.split(" ")
                    self.hue_min_green = int(green_col_val[0])
                    self.hue_max_green = int(green_col_val[1])
                    self.sat_min_green = int(green_col_val[2])
                    self.sat_max_green = int(green_col_val[3])
                    self.val_min_green = int(green_col_val[4])
                    self.val_max_green = int(green_col_val[5])
            self.lock.release()
        except:
            print("Failed to get colors from file")
        #print("YOU DID IT MAN, YOU'RE THE MAN OF THE MEN! HIGH FUCKING HIGH MOTHAFOCKAAAA")
        #print(data)

    def UpdateColors(self): 
        
        try:
            self.lock.acquire()
            self.last_col = "{0} {1} {2} {3} {4} {5}".format(self.hue_min, self.hue_max, self.sat_min, self.sat_max, self.val_min, self.val_max) 
            #str([self.hue_min, self.hue_max, self.sat_min, self.sat_max, self.val_min, self.val_max])
            #print(self.last_col)
            data = [
                "COLOR: h_min h_max s_min s_max v_min v_max;",
                " ",
                "LAST: " + self.last_col + ";",
                "BLUE: " + self.blue_col + ";",
                "YELLOW: " + self.yellow_col + ";",
                "GREEN: " + self.green_col + ";",
                "END"]

            f = open('test_color.txt', 'w')

            for l in range((len(data))):
                f.write(data[l] + "\n")
            f.close()
            self.lock.release()
        except:
            print("Failed to write colors to file")

    def ChangeHSVColor(self, color):
        if color == "LAST":
            self.hue_min = int(self.last_col_val[0])
            self.hue_max = int(self.last_col_val[1])
            self.sat_min = int(self.last_col_val[2])
            self.sat_max = int(self.last_col_val[3])
            self.val_min = int(self.last_col_val[4])
            self.val_max = int(self.last_col_val[5])
            

        elif color == "BLUE":
            self.hue_min = self.hue_min_blue
            self.hue_max = self.hue_max_blue
            self.sat_min = self.sat_min_blue
            self.sat_max = self.sat_max_blue
            self.val_min = self.val_min_blue
            self.val_max = self.val_max_blue

        elif color == "YELLOW":
            self.hue_min = self.hue_min_yellow
            self.hue_max = self.hue_max_yellow
            self.sat_min = self.sat_min_yellow
            self.sat_max = self.sat_max_yellow
            self.val_min = self.val_min_yellow
            self.val_max = self.val_max_yellow

        elif color == "GREEN":
            self.hue_min = self.hue_min_green
            self.hue_max = self.hue_max_green
            self.sat_min = self.sat_min_green
            self.sat_max = self.sat_max_green
            self.val_min = self.val_min_green
            self.val_max = self.val_max_green
        
        else:
            self.hue_min = self.ids.hue_min_slider.value
            self.hue_max = self.ids.hue_max_slider.value
            self.sat_min = self.ids.sat_min_slider.value
            self.sat_max = self.ids.sat_max_slider.value
            self.val_min = self.ids.val_min_slider.value
            self.val_max = self.ids.val_max_slider.value 

        self.ids.hue_min_label.text = "Hue min: " + str(self.hue_min)
        self.ids.hue_min_slider.value = self.hue_min
        self.ids.hue_max_label.text = "Hue max: " + str(self.hue_max)
        self.ids.hue_max_slider.value = self.hue_max

        self.ids.sat_min_label.text = "Sat min: " + str(self.sat_min)
        self.ids.sat_min_slider.value = self.sat_min
        self.ids.sat_max_label.text = "Sat max: " + str(self.sat_max)
        self.ids.sat_max_slider.value = self.sat_max  

        self.ids.val_min_label.text = "val min: " + str(self.val_min)
        self.ids.val_min_slider.value = self.val_min
        self.ids.val_max_label.text = "val max: " + str(self.val_max)
        self.ids.val_max_slider.value = self.val_max 


    def CaptureThread(self):
        self.CapThread = threading.Thread(target= self.buildIMG,daemon=True)
        self.CapThread.start()
        self.ids.btn_apply.disabled = False
        self.ids.btn_start_color.disabled = True

    def StopCaptureThread(self, *args):
        self.capture_clock.cancel()
        self.capture.release()
        cv2.destroyAllWindows()
        self.ids.btn_apply.disabled = True
        self.ids.btn_start_color.disabled = False

    def buildIMG(self):
        #self.img1=Image()
        self.capture = cv2.VideoCapture(0)
        self.capture_clock = Clock.schedule_interval(self.Update, 1.0/10.0)
        #Clock.schedule_once(self.StopCaptureThread,5)
        

    def Update(self, dt):
        ret, frame = self.capture.read()
        imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        self.lock.acquire()
        lower = np.array([self.hue_min, self.sat_min, self.val_min])
        upper = np.array([self.hue_max, self.sat_max, self.val_max])
        self.lock.release()
        frame = cv2.inRange(imgHSV, lower, upper)

        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='luminance') 
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
        texture.blit_buffer(frame.tobytes(order=None), colorfmt='luminance', bufferfmt='ubyte')
        texture.flip_vertical()
        self.ids.image.texture = texture


    def slide_hue_min(self, *args):
        #print(int(args[1]))
        self.hue_min = int(args[1])
        self.ids.hue_min_label.text = "Hue min: " + str(self.hue_min)
        #self.ColorPicker()
        #print(str(self.hue_min))
        #self.slide_text.font_size = str(int(args[1]) + 20)

    def slide_hue_max(self, *args):
        self.hue_max = int(args[1])
        self.ids.hue_max_label.text = "Hue max: " + str(self.hue_max)
        #self.ColorPicker()

    def slide_sat_min(self, *args):
        self.sat_min = int(args[1])
        self.ids.sat_min_label.text = "Sat min: " + str(self.sat_min)
        #self.ColorPicker()

    def slide_sat_max(self, *args):
        self.sat_max = int(args[1])
        self.ids.sat_max_label.text = "Sat max: " + str(self.sat_max)
        #self.ColorPicker()

    def slide_val_min(self, *args):
        self.val_min = int(args[1])
        self.ids.val_min_label.text = "Val min: " + str(self.val_min)
        #self.ColorPicker()

    def slide_val_max(self, *args):
        self.val_max = int(args[1])
        self.ids.val_max_label.text = "Val max: " + str(self.val_max)
        #self.ColorPicker()

    # Unused ATM
    def thread(self):
        threading.Thread(target = self.ColorPicker).start()

        #ColorPicker ikke i bruk
    # def ColorPicker(self):
    #     frameWidth = 640
    #     frameHeight = 480
    #     cap = cv2.VideoCapture(0)
    #     cap.set(3, frameWidth)
    #     cap.set(4, frameHeight)     
        
    #     ret, img = cap.read()
    #     if(ret):
    #         imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #         lower = np.array([self.hue_min, self.sat_min, self.val_min])
    #         upper = np.array([self.hue_max, self.sat_max, self.val_max])
    #         mask = cv2.inRange(imgHSV,lower,upper)
    #         cv2.imwrite('test.png', mask)
    #         cv2.imwrite('test1.png', mask)
    #         cv2.destroyAllWindows()
    #     else:
    #         print("nope niks neeei - prøv igjen")


class CalibrationWindow(Screen):
    font_size_pos = 50
    font_size_buttons = 20
    axis = "x"
    GoTo_ok = 1,0,0

    def NumPadPress(self, number): #[(70,620),(65,735)]
        if int(self.ids.text_x_pos.text) == 0 and self.axis == "x":
            self.ids.text_x_pos.text = str(number)
        elif int(self.ids.text_y_pos.text) == 0 and self.axis == "y":
            self.ids.text_y_pos.text = str(number)
        else:   
            if self.axis == "x":
                if number > -1:
                    self.ids.text_x_pos.text += str(number)
                else:
                    self.ids.text_x_pos.text = "0"

                if int(self.ids.text_x_pos.text) < 70 or int(self.ids.text_x_pos.text) > 620:
                    self.ids.text_x_pos.foreground_color = 1, 0, 0
                else:
                    self.ids.text_x_pos.foreground_color = 0, 0, 0
            else:   
                if number > -1:
                    self.ids.text_y_pos.text += str(number)
                else:
                    self.ids.text_y_pos.text = "0"
                
                if int(self.ids.text_y_pos.text) < 65 or int(self.ids.text_y_pos.text) > 735:
                    self.ids.text_y_pos.foreground_color = 1, 0, 0
                else:
                    self.ids.text_y_pos.foreground_color = 0, 0, 0

            if int(self.ids.text_x_pos.text) < 70 or int(self.ids.text_x_pos.text) > 620 or int(self.ids.text_y_pos.text) < 65 or int(self.ids.text_y_pos.text) > 735:
                self.ids.GoTo_btn.color = 1,0,0
            else:
                self.ids.GoTo_btn.color = 0,1,0

    def ChooseXYvalue(self, axis):
        if axis == 0:
            self.axis = "x"
        else:
            self.axis = "y"

    def GoTo_btn(self):
        if int(self.ids.text_x_pos.text) < 70 or int(self.ids.text_x_pos.text) > 620 or int(self.ids.text_y_pos.text) < 65 or int(self.ids.text_y_pos.text) > 735:
            PopUpGoTo()
        else: # send postitions to arduino
            pass
    
    
        

class SettingsWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass
class GoToPopopWindow(FloatLayout):
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

def PopUpGoTo():
        show = GoToPopopWindow()
        popupWindow = Popup(title="WARNING",content=show, size_hint=(None,None), size=(300,200))
        popupWindow.open()

class MyApp(App):
    def build(self):
        return kv


    #def on_start(self):
     #   Clock.schedule_once(self.)
        

# OLD OLD OLD OLD
#def run():
 #   if __name__ == "__main__":
  #      MyApp().run()

#x = threading.Thread(target=run)
#x.start()
# OLD OLD OLD OLD

if __name__ == "__main__":
    MyApp().run()


