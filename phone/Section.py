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
"""An android/pc/mac/ios app Module based on python-kivy for main menu to select .

    MATERIALS REQUIREMENTS :

        -   Required Kivy install and images folder for background buttons.
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from Login import Title
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from random import randrange

RSel = False
LSel = False

Builder.load_string('''
<FrameL>:
    canvas :
        Color :
            rgba : 0,0,0,1
        Rectangle :
            size : self.size
            pos : self.pos
''')


class CustomButtonR(ButtonBehavior, Image):
    # Custom button to make image act as button to select eyes'lookup
    def __init__(self, **kwargs):
        super(CustomButtonR, self).__init__(**kwargs)
        random_image = 'background_images/im' + str(randrange(18)) + '.jpg'
        self.source = random_image
        self.allow_stretch = True
        self.keep_ratio = False
        self.RSel = False

    def on_release(self):
        self.RSel = True


class CustomButtonL(ButtonBehavior, Image):
    # Custom button to make image act as button to select Logging
    def __init__(self, **kwargs):
        super(CustomButtonL, self).__init__(**kwargs)
        random_image = 'background_images/im' + str(randrange(18)) + '.jpg'
        self.source = random_image
        self.allow_stretch = True
        self.keep_ratio = False
        self.LSel = False

    def on_release(self):
        self.LSel = True


class FrameL(BoxLayout):
    # This is parent frame
    def set(self):
        self.orientation = 'vertical'
        self.padding = (10, 10)
        self.spacing = 10


class LabelF(Button):
    # This class create label at bottom of image
    def set(self, text):
        self.text = text
        self.background_normal = ''
        self.background_color = (1, .4392, .2627, 1)
        self.color = (0, 0, 0, 1)


class Main(BoxLayout):
    def set(self):
        # This function set all the objects in the class Main and set their appropiate values
        self.orientation = 'horizontal'
        self.R = CustomButtonR(size_hint=(1, .9))
        self.L = CustomButtonL(size_hint=(1, .9))
        self.RB = FrameL()
        self.RB.set()
        self.RL = LabelF(size_hint=(1, .1), on_press=self.ResS)
        self.RL.set("Eyes'looks")
        self.RB.add_widget(self.R)
        self.RB.add_widget(self.RL)
        self.LL = LabelF(size_hint=(1, .1), on_press=self.LogS)
        self.LL.set('Statistics')
        self.LB = FrameL()
        self.LB.set()
        self.LB.add_widget(self.L)
        self.LB.add_widget(self.LL)
        self.add_widget(self.RB)
        self.add_widget(self.LB)

    def ResS(self, s):
        # Fuction to tell that eyes'lookup is selected
        self.R.RSel = True

    def LogS(self, x):
        # Fuction to tell that Lodging is selected
        self.L.LSel = True


class SectionScreen(Screen, BoxLayout):
    def set(self):
        # Section Screen set the values to approprate postion
        self.name = 'section'
        self.orientation = 'vertical'
        self.T = Title()
        self.T.set()
        self.add_widget(self.T, index=0)
        self.m = Main(size_hint=(1, .9))
        self.m.set()
        self.add_widget(self.m, index=0)


class SectionApp(App):
    # SectionApp create application of individual application to run
    def build(self):
        self.sm = ScreenManager()
        self.s = SectionScreen()
        self.s.set()
        self.sm.add_widget(self.s)
        return self.sm


if __name__ == '__main__':
    SectionApp().run()
