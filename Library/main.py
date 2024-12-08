from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import subprocess
import sys
from threading import Thread
import message



Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '500')

Config.set('graphics', 'resizable', True)

from kivy.core.window import Window
Window.clearcolor = get_color_from_hex('#33bbff')



# creating the App class
class MyApp(App):

    def on_start(self):
        self.title = 'Login to VirtualLibrary'

    def build(self):

        self.name_label1 = Label(text="e-mail:", font_size=20, pos=(260, 310))
        self.name_input1 = TextInput(size=(200, 30), pos=(350, 345))
        self.name_label2 = Label(text="password:", font_size=20, pos=(255, 245))
        self.name_input2 = TextInput(password=True,size=(200, 30), pos=(350, 280))

        self.img1 = Image(source='Images/person.png',size=(170,170))

        # Setam pozitia
        self.img1.pos = (340, 420)
        self.img1.opacity = 1

        # adding image 1 to widget
        s = Widget()
        s.add_widget(self.img1)

        # add Lable and Input Text to widget
        s.add_widget(self.name_label1)
        s.add_widget(self.name_input1)
        s.add_widget(self.name_label2)
        s.add_widget(self.name_input2)


        def on_button1_press(instance):
            instance.background_down = 'Images/power_down.png'  # Setăm imaginea pentru starea apăsata
            message.close_window()



        # loading image 2 as a button
        button1= Button(background_normal='Images/power.png', pos=(30, 20), size_hint=(None, None), size=(70, 70))
        button1.bind(on_press=on_button1_press)
        # adding button to widget
        s.add_widget(button1)

        # add button login
        button2=Button(background_normal='Images/button_login _down.png', pos=(340, 160), size_hint=(None, None), size=(140, 60))
        button2.bind(on_press=self.on_button2_press)
        s.add_widget(button2)
        # return widget
        return s

    def on_button2_press(self,obj):
        obj.background_down = 'Images/button_login _up.png'
        val=message.login(self.name_input1.text, self.name_input2.text)
        self.name_input1.text=''
        self.name_input2.text = ''
        if(val==True):
            Thread(target=lambda: subprocess.run([sys.executable, 'agenda_books.py'])).start()
        else:
            self.name_input2.text = ''
            message.warning("Warning!","E_mail or password is WRONG!!")

# run the app
MyApp().run()