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
"""The main graphic module to open run server or perform administrativs task .

    IMPORTS :
        -   controler.datasetCreator as InputFeature
        -   server import main as LaunchServer


    MATERIALS REQUIREMENTS :

        -   Required server port not use tkinter install and be in same folfer with server file .
"""


import tkinter as tk
from tkinter import messagebox
import time
from serverCom2phone import main as LaunchServer
import threading


LARGE_FONT = ("Verdana", 12)

nameOfAdmin = str()


class Page(tk.Tk):
    """This clss manage all the windows and transitions between them

    ARGS :

        -   *args
        -   **Kwargs
    """

    def __init__(self, *args, **Kwargs):
        """This method is responsible to ::
                -   set the first showing frame (tkinter window)
                -   save other frame in a list
                -   launch the starter frame (PageOne)
        """
        tk.Tk.__init__(self, *args, **Kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in [StartPage, PageOne]:
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        """This method is responsible to ::
                -   show a specific frame
        """
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    """This class set and configure widgets for the stater frame which is the login page
    ARGS :

        -   parent
        -   controller
    """
    def __init__(self, parent, controller):
        """This method is responsible to ::
                -   set the first showing frame (tkinter window)
        """
        tk.Frame.__init__(self, parent)
        global nameOfAdmin

        l_title = tk.Label(self, text="Acces Serveur", font="Arial,12")
        l_title.grid(row=0, column=0, columnspan=3, sticky="NSEW", padx=30, pady=30)

        checkboxLang1 = tk.Checkbutton(self, text="FR")
        checkboxLang1.grid(row=0, column=2, sticky='NSEW', padx=10, pady=10)

        checkboxLang2 = tk.Checkbutton(self, text="ENG")
        checkboxLang2.grid(row=0, column=3, sticky='NSEW', padx=10, pady=10)

        label_username = tk.Label(self, text="Login")
        label_password = tk.Label(self, text="Password")

        entry_username = tk.Entry(self)

        entry_password = tk.Entry(self, show="*")

        label_username.grid(row=2, column=0, sticky='NSEW', padx=10, pady=10)
        label_password.grid(row=3, column=0, sticky='NSEW', padx=10, pady=10)
        entry_username.grid(row=2, column=1, sticky='NSEW', padx=10, pady=10)
        entry_password.grid(row=3, column=1, sticky='NSEW', padx=10, pady=10)

        checkbox = tk.Checkbutton(self, text="Keep me logged in")
        checkbox.grid(row=4, column=1, sticky='NSEW', padx=10, pady=10)

        logbtn = tk.Button(self, text="Login", bg="BlACK", fg="White", command=lambda: login_btn_clicked())
        logbtn.grid(row=5, column=1, sticky='NSEW', padx=10, pady=10)

        def login_btn_clicked():
            """This method is responsible an await events function actioned by a click ::
                    -   get the login an password
                    -   compare with what is in database
                    -   allow/disable access to the next page
                    -   show a pupup info if parameters wrongs
            """
            # print("Clicked")
            username = entry_username.get()
            password = entry_password.get()

            if ((len(username) > 2) and (len(password) >= 8)):

                if username == "admin" and password == "adminBEP":
                    controller.show_frame(PageOne)
                # display a ,essage if username and password is incorrect!
                else:
                    messagebox.showinfo(self, "Login ou password Invalide ! ")

            else:
                messagebox.showinfo(self, "Entrer Un Login Ou password")


class PageOne(tk.Frame):
    """This class set and configure widgets for the menu frame
    ARGS :

        -   parent
        -   controller
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global nameOfAdmin

        serverbtn = Serverbtn()
        server_btn = Serverbtn(self, text="sever On/Off", bg="red", fg="White", command=lambda:serverbtn.start_server(),
                               clickedbg='green')
        server_btn.grid(row=2, column=3, sticky='NSEW', padx=10, pady=10)

        clock = tk.Label(self, font=('times', 18, 'bold'), bg='gray', fg="white")
        clock.grid(row=0, column=2, sticky="NSNESWSE", padx=8, pady=8)

        def tick():
            """This methods show time in the specific time format('%H:%M:%S')"""
            time2 = time.strftime('%H:%M:%S')
            clock.config(text=time2)
            clock.after(200, tick)

        tick()

        nameOfAdmin = "Espace Admin" + nameOfAdmin
        label = tk.Label(self, text=nameOfAdmin, font="Arial,16")
        label.grid(row=0, column=0, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

        def runner():
            global after_id
            global secs
            secs += 1
            if secs % 2 == 0:  # every other second
                e_host_v = e_host.get()
                e_port_v = int(e_port.get())

            # after_id = self.after(1000, runner)  # check again in 1 second



class Serverbtn(tk.Button):
    """This class set and configure widgets for the menu frame
    ARGS :

        -   master=None
        -   **Kw
    """
    def __init__(self, master=None, **Kw):
        self.clicked_color = Kw.pop('clickedbg', 'green')
        tk.Button.__init__(self, master, **Kw)
        self.bind('<Button-1>', self.clicked)

    def clicked(self, *args):
        """This methods change the button color if clicked
            ARGS :
                -  *args
        """
        self['bg'] = self.clicked_color

    def start_server(self):
        """This methods run the server code to wait cliients connections"""
        thr_loadserver = threading.Thread(target=LaunchServer)  # allow work in background and in tkinter window
        thr_loadserver.start()


app = Page()
app.mainloop()
