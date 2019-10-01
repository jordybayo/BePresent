# Copyright 2019 The Bayo. All Rights Reserved.
#
# Licensed under the Bayobrain License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.bayobrain.org/licenses/LICENSE-1.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""An android/pc/mac/ios app Module based on python-kivy for running presences verifications.

    MATERIALS REQUIREMENTS :

        -   Required Kivy install and the teacher sqlite.db database to extract information that have been saved.
"""

from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import sqlite3

connection = sqlite3.connect('bepresentteach.db')

conn = connection.cursor()

Builder.load_string('''
<ResTitle>:
    orientation: 'vertical'
    size_hint : 1, .1
    canvas:
        Color :
            rgba : .9411,.3843,.5725,1
        Rectangle:
            size : self.size
            pos : self.pos
    Label:
        text : "Resturant"
        color : 0,0,0,1
        bold : True
        font_size : 50


<Orders>:
    canvas:
        Color:
            rgba : 0,1,1,1
        Rectangle:
            size : self.size
            pos : self.pos

<Hist>:
    BoxLayout:
        id:box
        orientation:'vertical'
        size_hint_y:None
        height:self.minimum_height
            

<AccTypeDay>:
    Button:
        text : '1'
        size_hint_y : None
        height : 36
        on_release : root.select('01')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '2'
        size_hint_y : None
        height : 36
        on_release : root.select('02')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '3'
        size_hint_y : None
        height : 36
        on_release : root.select('03')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '4'
        size_hint_y : None
        height : 36
        on_release : root.select('04')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '5'
        size_hint_y : None
        height : 36
        on_release : root.select('05')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '6'
        size_hint_y : None
        height : 36
        on_release : root.select('06')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '7'
        size_hint_y : None
        height : 36
        on_release : root.select('07')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '8'
        size_hint_y : None
        height : 36
        on_release : root.select('08')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '9'
        size_hint_y : None
        height : 36
        on_release : root.select('09')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '10'
        size_hint_y : None
        height : 36
        on_release : root.select('10')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '11'
        size_hint_y : None
        height : 36
        on_release : root.select('11')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '12'
        size_hint_y : None
        height : 36
        on_release : root.select('12')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '13'
        size_hint_y : None
        height : 36
        on_release : root.select('13')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '14'
        size_hint_y : None
        height : 36
        on_release : root.select('14')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '15'
        size_hint_y : None
        height : 36
        on_release : root.select('15')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '16'
        size_hint_y : None
        height : 36
        on_release : root.select('17')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '18'
        size_hint_y : None
        height : 36
        on_release : root.select('18')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '19'
        size_hint_y : None
        height : 36
        on_release : root.select('19')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '20'
        size_hint_y : None
        height : 36
        on_release : root.select('20')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '21'
        size_hint_y : None
        height : 36
        on_release : root.select('21')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '22'
        size_hint_y : None
        height : 36
        on_release : root.select('22')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '23'
        size_hint_y : None
        height : 36
        on_release : root.select('23')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '24'
        size_hint_y : None
        height : 36
        on_release : root.select('24')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '25'
        size_hint_y : None
        height : 36
        on_release : root.select('25')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '26'
        size_hint_y : None
        height : 36
        on_release : root.select('26')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '27'
        size_hint_y : None
        height : 36
        on_release : root.select('27')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '28'
        size_hint_y : None
        height : 36
        on_release : root.select('28')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '29'
        size_hint_y : None
        height : 36
        on_release : root.select('29')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '30'
        size_hint_y : None
        height : 36
        on_release : root.select('30')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '31'
        size_hint_y : None
        height : 36
        on_release : root.select('31')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
        
        
<AccTypeMonth>:
    Button:
        text : 'September'
        size_hint_y : None
        height : 36
        on_release : root.select('09')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : 'October'
        size_hint_y : None
        height : 36
        on_release : root.select('10')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : 'November'
        size_hint_y : None
        height : 36
        on_release : root.select('11')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : 'December'
        size_hint_y : None
        height : 36
        on_release : root.select('12')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : 'January'
        size_hint_y : None
        height : 36
        on_release : root.select('01')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : 'Febuary'
        size_hint_y : None
        height : 36
        on_release : root.select('02')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : 'March'
        size_hint_y : None
        height : 36
        on_release : root.select('03')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : 'April'
        size_hint_y : None
        height : 36
        on_release : root.select('04')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : 'May'
        size_hint_y : None
        height : 36
        on_release : root.select('05')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : 'June'
        size_hint_y : None
        height : 36
        on_release : root.select('06')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : 'July'
        size_hint_y : None
        height : 36
        on_release : root.select('07')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1


<AccTypeYear>:
    Button:
        text : '2019'
        size_hint_y : None
        height : 36
        on_release : root.select('2019')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '2020'
        size_hint_y : None
        height : 36
        on_release : root.select('2020')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '2021'
        size_hint_y : None
        height : 36
        on_release : root.select('2021')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '2022'
        size_hint_y : None
        height : 36
        on_release : root.select('2022')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '2023'
        size_hint_y : None
        height : 36
        on_release : root.select('2023')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '2024'
        size_hint_y : None
        height : 36
        on_release : root.select('2024')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : '2025'
        size_hint_y : None
        height : 36
        on_release : root.select('2025')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
''')




class Check_popup(Popup):
    # Show pop up if encounter error in the filling parameters
    def set(self):
        self.title = 'Not Filled'
        self.content = Label(text='wrong Values Details')
        self.size_hint = (None, None)
        self.size = (200, 200)

class PopUp(Popup):
    # Show pop up if encounter error in the login
    def set(self):
        self.title = 'Wrong Login Details'
        self.content = Label(text='Login or password invalid')
        self.size_hint = (None, None)
        self.size = (200, 200)

class AccTypeDay(DropDown):
    # To create drop down list
    pass

class AccTypeMonth(DropDown):
    # To create drop down list
    pass

class AccTypeYear(DropDown):
    # To create drop down list
    pass


class UP(BoxLayout):
    # Frame grouping label and input for login
    def set(self):
        self.padding = (5, 5)
        self.spacing = 10

    def asetDay(self):
        self.add_widget(Label(text='Day', color=(0, 0, 0, 1)))
        self.Account = AccTypeDay()
        self.acc = Button(text='DD', background_normal='', background_color=(1, .4392, .2627, 1),
                          color=(0, 0, 0, 1))
        self.acc.bind(on_release=self.Account.open)
        self.Account.bind(on_select=lambda instance, x: setattr(self.acc, 'text', x))
        self.add_widget(self.acc)
        self.set()

    def asetMonth(self):
        self.add_widget(Label(text='Month', color=(0, 0, 0, 1)))
        self.Account = AccTypeMonth()
        self.acc = Button(text='MM', background_normal='', background_color=(1, .4392, .2627, 1),
                          color=(0, 0, 0, 1))
        self.acc.bind(on_release=self.Account.open)
        self.Account.bind(on_select=lambda instance, x: setattr(self.acc, 'text', x))
        self.add_widget(self.acc)
        self.set()

    def asetYear(self):
        self.add_widget(Label(text='Year', color=(0, 0, 0, 1)))
        self.Account = AccTypeYear()
        self.acc = Button(text='YYYY', background_normal='', background_color=(1, .4392, .2627, 1),
                          color=(0, 0, 0, 1))
        self.acc.bind(on_release=self.Account.open)
        self.Account.bind(on_select=lambda instance, x: setattr(self.acc, 'text', x))
        self.add_widget(self.acc)
        self.set()

    def oset(self, t, f):
        self.add_widget(Label(text=t + ' : ', color=(0, 0, 0, 1)))
        self.I = TextInput(hint_text=t, multiline=False, padding=(10, 10), password=f)
        self.add_widget(self.I)
        self.set()


class Orders(BoxLayout):
    """Class That give possibility to launch the presences looking Process"""

    def set(self):
        self.orientation = 'vertical'
        self.size_hint = (.3, 1)
        self.padding = (10, 10)
        self.spacing = 10
        self.bk = False
        self.SignUpT = True
        self.LoginT = False
        self.padding = (10, 10)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.aw(Label(text='History', color=(0, 0, 0, 1), bold=True, font_size=25))

        self.ASD = UP()
        self.ASD.asetDay()
        self.aw(self.ASD)

        self.ASM = UP()
        self.ASM.asetMonth()
        self.aw(self.ASM)

        self.ASY = UP()
        self.ASY.asetYear()
        self.aw(self.ASY)

        self.lg = Button(text='See', on_press=self.stl, background_normal='', background_color=(1, .4392, .2627, 1),
                         color=(0, 0, 0, 1))
        self.aw(self.lg)

    def aw(self, ob):
        self.add_widget(ob)

    def stl(self, instance):
        """wait if there is a wrong fill or else show loading popup and then the result"""

        stud_list = []
        if self.ASD.acc.text != '' and self.ASM.acc.text != '' and self.ASY.acc.text != '':
            historique = self.ASY.acc.text + '-' + self.ASM.acc.text + '-' + self.ASD.acc.text
            conn.execute("SELECT * FROM attendances")  # WHERE datetime = '{}'".format(historique))
            connection.commit()
            self.validcheck = conn.fetchall()
            for a in self.validcheck:
                for b in a:
                    separate_datetime = str(b).split(' ')
                    if str(separate_datetime[0]) == str(historique):
                        stud_list.append(a[1])

            self.attendaces(students_list=stud_list)   # show attendances
        else:
            self.cp = Check_popup()
            self.cp.set()
            self.cp.open()

    def back(self, a):
        self.bk = True

    def attendaces(self, students_list):
        """This function show the Students Attendances List to the teacher"""
        # scrollview all the names
        self.aw(Label(text='Attendances List', color=(21, 91, 218, 1), bold=True, font_size=25))

        self.story = BoxLayout(orientation='vertical', height=400, size_hint=(.5, 1))
        self.story.add_widget(Hist(students_list))
        self.add_widget(self.story)

        self.sbl = BoxLayout(orientation='horizontal', size_hint=(1, None), height=15)
        self.sbl.add_widget(Button(text='back', size_hint=(.5, 1), on_press=self.back))
        self.add_widget(self.sbl)
        self.shown = []
        self.obj = []

    def up(self, a):
        pass


class Hist(ScrollView):
    def __init__(self, students_list, **kwargs):
        super().__init__(**kwargs)
        for students in students_list:
            self.ids.box.add_widget(Label(text=students, font_size=14, italic=True, size_hint_y=None, height=40, color=(0, 0, 0, 1)))


class ResBg(BoxLayout):
    def set(self):
        self.o = Orders()
        self.o.set()
        self.add_widget(self.o)


class ResTitle(BoxLayout):
    # Main title of the Application
    def set(self):
        self.size_hint = (1, .1)
        self.pos_hint = {'top': 1, 'center_x': 0.5}


class LodScreen(Screen, BoxLayout):
    def set(self):
        self.name = "LodgingScreen"
        self.orientation = 'vertical'
        self.Ti = ResTitle()
        self.Ti.set()
        self.add_widget(self.Ti)
        self.rb = ResBg()
        self.rb.set()
        self.add_widget(self.rb)
        self.show_popup = PopUp()
        self.show_popup.set()


class ResScreenM(ScreenManager):
    def set(self):
        self.R = LodScreen()
        self.R.set()
        self.add_widget(self.R)


class ResScreenApp(App):
    def build(self):
        self.s = ResScreenM()
        self.s.set()
        Clock.schedule_interval(self.s.R.rb.o.up, 1.0 / 60.0)
        inspector.create_inspector(Window, self.s)
        return self.s


if __name__ == '__main__':
    ResScreenApp().run()
