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

from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.stacklayout import StackLayout
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
from clientCom2rasp import SaveStudent
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

<Att>:
    BoxLayout:
        id:box
        orientation:'vertical'
        size_hint_y:None
        height:self.minimum_height
    
            
<Order>:
    canvas:
        Color:
            rgba : 0,0,0,1
        Rectangle:
            size: self.size
            pos : self.pos
            
<AccType>:
    Button:
        text : 'AMPHI1'
        size_hint_y : None
        height : 36
        on_release : root.select('AMPHI1')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : 'AMPHI2'
        size_hint_y : None
        height : 36
        on_release : root.select('AMPHI2')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : 'Laboratoire CISCO'
        size_hint_y : None
        height : 36
        on_release : root.select('Laboratoire CISCO')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : 'GI1 Batiment C'
        size_hint_y : None
        height : 36
        on_release : root.select('AMPHI3')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
    Button:
        text : 'GI2-GL Batiment A'
        size_hint_y : None
        height : 36
        on_release : root.select('AMPHI3')
        background_normal: ''
        background_color : 1,.4392,.2627,1
        color : 0,0,0,1
''')
cartitem = []
nud = False


class Order(BoxLayout):
    def set(self, item):
        self.rm = False
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = 44
        self.name = Label(text=item[0], size_hint=(.4, 1))
        self.add_widget(self.name)
        self.quantity = Label(text=str(item[2]), size_hint=(.3, 1))
        self.add_widget(self.quantity)
        self.price = Label(text=str(int(item[2]) * int(item[1])), size_hint=(.2, 1))
        self.add_widget(self.price)
        self.remove = Button(text="X", size_hint=(.1, 1), on_press=self.removeOrder)
        self.add_widget(self.remove)
        return self

    def removeOrder(self, a):
        self.rm = True


class Loading(Popup):
    # Show pop up if encounter error in the login
    def set(self, title, message):
        self.title = title
        self.content = Label(text=message)
        self.size_hint = (None, None)
        self.size = (300, 200)


class PopUp(Popup):
    # Show pop up if encounter error in the login
    def set(self):
        self.title = 'Intelligence Acting'
        self.content = Label(text='please wait.. \nIm looking for students present')
        self.size_hint = (None, None)
        self.size = (300, 200)
        self.pos_hint = {'top': 0, 'center_x': 0.5, 'center': 1}


class Check_popup(Popup):
    # Show pop up if encounter error in the filling parameters
    def set(self):
        self.title = 'Blancs not Filled'
        self.content = Label(text='You have entered \n wrong Values Details')
        self.size_hint = (None, None)
        self.size = (200, 200)


class AccType(DropDown):
    # To create drop down list
    pass


class UP(BoxLayout):
    # Frame grouping label and input for login
    def set(self):
        self.padding = (5, 5)
        self.spacing = 10

    def aset(self):
        self.add_widget(Label(text='Classroom Name', color=(0, 0, 0, 1)))
        self.Account = AccType()
        self.acc = Button(text='Select classroom. Name', background_normal='', background_color=(1, .4392, .2627, 1),
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
        self.aw(Label(text='look For Students present in Class', color=(0, 0, 0, 1), bold=True, font_size=25))
        self.AS = UP()
        self.AS.aset()
        self.aw(self.AS)
        self.TI = UP()
        self.TI.oset('teacher Id', False)
        self.aw(self.TI)
        self.CN = UP()
        self.CN.oset('Course Name', False)
        self.aw(self.CN)
        self.SP = UP()
        self.SP.oset('Speciality or Depart', False)
        self.aw(self.SP)
        self.lg = Button(text='Start', on_press=self.stl, background_normal='', background_color=(1, .4392, .2627, 1),
                         color=(0, 0, 0, 1))
        self.aw(self.lg)

    def aw(self, ob):
        self.add_widget(ob)

    def stl(self, instance):
        """wait if there is a wrong fill or else show loading popup and then the result"""

        with open("FILES/asyncwait.ph", "w") as fic:
            fic.write("1")  # the value in the file determine how long will the loading show
            fic.close()
        if self.TI.I.text != '' and self.CN.I.text != '' and self.SP.I.text != '' and self.AS.acc.text != '':
            self.stl = SaveStudent(self.AS.acc.text, self.TI.I.text, self.CN.I.text, self.SP.I.text)
            self.stl.send_detection_starting()

            self.cp = Loading()
            self.cp.set('Intelligence Acting', 'please wait.. (@ @) \n Im looking at students present')
            self.cp.open()
            loading = True
            while loading:
                with open("FILES/asyncwait.ph", "r") as fic:
                    asyncwait_bool_var = fic.read()
                    fic.close()
                    if asyncwait_bool_var is '0':
                        loading = False
            self.cp = None
            self.attendances()  # show attendances
        else:
            self.cp = Check_popup()
            self.cp.set()
            self.cp.open()

    def back(self, a):
        self.bk = True

    def attendances(self):
        """This function show the Students Attendances List to the teacher"""

        self.aw(Label(text='Attendances List', color=(21, 91, 218, 1), bold=True, font_size=25))
        with open("FILES/currentAttce.ph", "r") as fic:
            students_list = fic.readlines()
            fic.close()

        self.att = BoxLayout(orientation='vertical', height=400, size_hint=(.5, 1))
        self.att.add_widget(Att(students_list))  # scrollview all the names
        self.add_widget(self.att)

        self.sbl = BoxLayout(orientation='horizontal', size_hint=(1, None), height=15)
        self.sbl.add_widget(Button(text='Save', size_hint=(.5, 1), on_press=self.save))
        self.sbl.add_widget(Button(text='back', size_hint=(.5, 1), on_press=self.back))
        self.add_widget(self.sbl)
        self.shown = []
        self.obj = []

    def up(self, a):
        pass

    def save(self, a):
        with open("FILES/currentAttce.ph", "r") as fic:
            all_students = fic.readlines()
            fic.close()

        conn.execute("SELECT strftime('%s','now')")
        str_Ftime = conn.fetchone()
        conn.execute("SELECT datetime({}, 'unixepoch', 'localtime')".format(str_Ftime[0]))
        date_time = conn.fetchone()
        for v in all_students:
            if v != "\n":
                self.query = 'INSERT INTO attendances VALUES ('
                self.query += "'{}'".format(date_time[0])
                self.query += ','
                self.query += "'" + v + "'"
                self.query += ')'
                conn.execute(self.query)  # inserting data in attendances Table
                connection.commit()
        connection.close()
        self.cp = Loading()
        self.cp.set('Great :)', 'Save Succcessfully..')
        self.cp.open()


class Att(ScrollView):
    def __init__(self, students_list, **kwargs):
        super().__init__(**kwargs)
        for students in students_list:
            self.ids.box.add_widget(
                Label(text=students, font_size=14, italic=True, size_hint_y=None, height=40, color=(0, 0, 0, 1)))


class ResBg(BoxLayout):
    def set(self):
        # self.orientation = 'horizontal'
        # self.size_hint = (1,.9)
        # self.m = ResMenu()
        # self.m.set()
        self.o = Orders()
        self.o.set()
        self.add_widget(self.o)
        # self.add_widget(self.m)


class ResTitle(BoxLayout):
    # Main title of the Application
    def set(self):
        self.size_hint = (1, .1)
        self.pos_hint = {'top': 1, 'center_x': 0.5}


class ResScreen(Screen, BoxLayout):
    def set(self):
        self.name = "CustResScreen"
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
        self.R = ResScreen()
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
