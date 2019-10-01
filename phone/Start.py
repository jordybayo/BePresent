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
"""An android/pc/mac/ios app Module based on python-kivy. Is the stater file for login the app.

    MATERIALS REQUIREMENTS :

        -   Required Kivy install and the teacher sqlite.db database to extract information that have been saved.
"""

import Login
from SignUp import SignUpScreen
from Section import SectionScreen
from Resturant import ResScreen
from Lodging import LodScreen
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.clock import Clock

class SwitchScreen(ScreenManager):
    # Switch Screen is the main screen manager of the application
    def loginC(self):
        self.L = Login.LoginScreen()
        self.L.set()
        self.add_widget(self.L)
        self.current = 'login'
        self.SU = SignUpScreen()
        self.SU.set()
        self.add_widget(self.SU)
        self.SE = SectionScreen()
        self.SE.set()
        self.add_widget(self.SE)
        self.RS = ResScreen()
        self.RS.set()
        self.add_widget(self.RS)
        self.LS = LodScreen()
        self.LS.set()
        self.add_widget(self.LS)
    def update(self,dt):
        # Checks if there is any change in the screen
        if self.LS.rb.o.bk == True or self.RS.rb.o.bk == True:
            self.current = 'section'
            self.SE.m.L.LSel = False
            self.LS.bk = False
            self.RS.rb.o.bk = False
            self.SE.m.R.RSel = False
        elif self.SE.m.R.RSel == True and self.L.B.LMB.LM.LoginT == True:
            self.current = "CustResScreen"
        elif self.SE.m.L.LSel == True:
            self.current = "LodgingScreen"
        elif self.L.B.LMB.LM.LoginT == True :
            self.current = 'section'
        elif self.L.B.LMB.LM.SignUpT == True :
            self.current = 'signup'
            if self.SU.X.SL.su.backtl == True or self.SU.X.SL.su.signupT == True:
                self.L.B.LMB.LM.SignUpT = False
                self.current = 'login'
                self.SU.X.SL.su.backtl = False
                self.SU.X.SL.su.signupT = False


class BePresent(App):
    # main application
    def build (self):
        self.a = SwitchScreen()
        self.a.loginC()
        Clock.schedule_interval(self.a.LS.rb.o.up,1.0 / 10.0)
        Clock.schedule_interval(self.a.update, 1.0 / 60.0)
        Clock.schedule_interval(self.a.RS.rb.o.up,1.0 / 30.0)
        return self.a

if __name__==  '__main__':
    BePresent().run()
