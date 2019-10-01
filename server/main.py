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
import pymysql.cursors
import hashlib
import controler.datasetCreator as InputFeature
import os
from server import main as LaunchServer
import threading

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='bepresent_pers',
                             password='password',
                             db='bepresent',
                             port=3306,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor
                             )

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

        for F in [StartPage, PageOne, RegisterStudent, RegisterAdmin, RegisterDepartment, RegisterClassrooms,
                  RegisterLevels, RegisterTeachers, RegisterCourses]:
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
            print(username, password)
            try:
                with connection.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT nom, nomUtilisateur, motPasse FROM Personnel_bepresent WHERE nomUtilisateur=%s"
                    cursor.execute(sql, (username,))
                    result = cursor.fetchone()
                    nameOfAdmin = str(result['nom'])  # this line doesn't give actually
            finally:
                pass

            if ((len(username) > 2) and (len(password) >= 8)):

                if username == result["nomUtilisateur"] and password == result["motPasse"]:
                    controller.show_frame(PageOne)
                # display a ,essage if username and password is incorrect!
                else:
                    messagebox.showinfo(self, "Username ou password Invalide ! ")

            else:
                messagebox.showinfo(self, "Entrer Un Username Ou password")


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
        server_btn.grid(row=0, column=3, sticky='NSEW', padx=10, pady=10)

        saveAdmin_btn = tk.Button(self, text="Enregistrer un Administrateur", bg="BlACK", fg="White",
                                 command=lambda: saveAdmin_btn_clicked())
        saveAdmin_btn.grid(row=2, column=1, sticky='NSEW', padx=10, pady=10)

        saveClass_btn = tk.Button(self, text="Enregistrer les Salles", bg="BlACK", fg="White",
                                 command=lambda: saveClass_btn_clicked())
        saveClass_btn.grid(row=3, column=1, sticky='NSEW', padx=10, pady=10)

        saveDepart_btn = tk.Button(self, text="Enregistrer les departements", bg="BlACK", fg="White",
                                 command=lambda: saveDepart_btn_clicked())
        saveDepart_btn.grid(row=4, column=1, sticky='NSEW', padx=10, pady=10)

        saveLevels_btn = tk.Button(self, text="Enregistrer les niveaux d'etude", bg="BlACK", fg="White",
                                 command=lambda: saveLevels_btn_clicked())
        saveLevels_btn.grid(row=5, column=1, sticky='NSEW', padx=10, pady=10)

        saveTeachers_btn = tk.Button(self, text="Enregistrer les Enseignants", bg="BlACK", fg="White",
                                 command=lambda: saveTeachers_btn_clicked())
        saveTeachers_btn.grid(row=6, column=1, sticky='NSEW', padx=10, pady=10)

        saveCourses_btn = tk.Button(self, text="Enregistrer les matieres", bg="BlACK", fg="White",
                                 command=lambda: saveCourses_btn_clicked())
        saveCourses_btn.grid(row=7, column=1, sticky='NSEW', padx=10, pady=10)

        saveAdmin_btn = tk.Button(self, text="Enregistrer un Etudiant", bg="BlACK", fg="White",
                                 command=lambda: saveStud_btn_clicked())
        saveAdmin_btn.grid(row=8, column=1, sticky='NSEW', padx=10, pady=10)

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


        def saveAdmin_btn_clicked():
            """This methods show the next page as saveAdmin_btn_clicked frame if button is clicked"""
            controller.show_frame(RegisterStudent)

        def saveAdmin_btn_clicked():
            """This methods show the next page as saveAdmin_btn_clicked frame if button is clicked"""
            controller.show_frame(RegisterAdmin)

        def saveDepart_btn_clicked():
            """This methods show the next page as saveDepart_btn_clicked frame if button is clicked"""
            controller.show_frame(RegisterDepartment)

        def saveClass_btn_clicked():
            """This methods show the next page as saveClass_btn_clicked frame if button is clicked"""
            controller.show_frame(RegisterClassrooms)

        def saveLevels_btn_clicked():
            """This methods show the next page as saveLevels_btn_clicked frame if button is clicked"""
            controller.show_frame(RegisterLevels)

        def saveTeachers_btn_clicked():
            """This methods show the next page as saveTeachers_btn_clicked frame if button is clicked"""
            controller.show_frame(RegisterTeachers)

        def saveCourses_btn_clicked():
            """This methods show the next page as saveCourses_btn_clicked frame if button is clicked"""
            controller.show_frame(RegisterCourses)

        def saveStud_btn_clicked():
            """This methods show the next page as saveStud_btn_clicked frame if button is clicked"""
            controller.show_frame(RegisterStudent)


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


class RegisterStudent(tk.Frame):
    """This class set and configure widgets to regisrter a student. the 'reconnaissance' button create the stud dataset
    ARGS :

        -   tk.Frame
        -   parent
        -   controller
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.var_txt_mat = tk.StringVar()
        self.var_txt_name = tk.StringVar()  # get Text variables
        self.var_txt_lname = tk.StringVar()
        self.var_txt_level = tk.IntVar()
        self.var_txt_spec = tk.StringVar()
        try:
            os.remove("FILES/currentReconn_ID.svr")
        except IOError as e:
            print("can't delete FILES/currentReconn_ID.svr : " + str(e))

        label = tk.Label(self, text="Enregistrer Un Etudiant", font="Arial,16")
        label.grid(row=0, column=0, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

        label_matricule = tk.Label(self, text="Matricule Etudiant")
        label_name = tk.Label(self, text="Nom")
        label_lastname = tk.Label(self, text="Prenom")
        label_username = tk.Label(self, text="Niveau")
        label_password = tk.Label(self, text="Specialite")

        entry_matricule = tk.Entry(self, textvariable=self.var_txt_mat)  # entry text
        entry_name = tk.Entry(self, textvariable=self.var_txt_name)
        entry_lastname = tk.Entry(self, textvariable=self.var_txt_lname)
        entry_level = tk.Entry(self, textvariable=self.var_txt_level)
        entry_spec = tk.Entry(self, textvariable=self.var_txt_spec)

        label_matricule.grid(row=2, column=0, sticky='NSEW', padx=10, pady=10)  # position of labels
        label_name.grid(row=3, column=0, sticky='NSEW', padx=10, pady=10)
        label_lastname.grid(row=4, column=0, sticky='NSEW', padx=10, pady=10)
        label_username.grid(row=5, column=0, sticky='NSEW', padx=10, pady=10)
        label_password.grid(row=6, column=0, sticky='NSEW', padx=10, pady=10)

        entry_matricule.grid(row=2, column=1, sticky='NSEW', padx=10, pady=10)  # position of entry text
        entry_name.grid(row=3, column=1, sticky='NSEW', padx=10, pady=10)
        entry_lastname.grid(row=4, column=1, sticky='NSEW', padx=10, pady=10)
        entry_level.grid(row=5, column=1, sticky='NSEW', padx=10, pady=10)
        entry_spec.grid(row=6, column=1, sticky='NSEW', padx=10, pady=10)

        backbtn = tk.Button(self, text="Reconnaissance", bg="blue", fg="White", command=lambda: self.recon_btn_clicked())
        backbtn.grid(row=6, column=2, sticky='NSEW', padx=10, pady=10)

        saveStudbtn = tk.Button(self, text="Sauveguarder", bg="BlACK", fg="White",
                                command=lambda: self.saveAdmin_btn_clicked())  # save btn
        saveStudbtn.grid(row=8, column=1, sticky='NSEW', padx=10, pady=10)

        backbtn = tk.Button(self, text="Retour", bg="BlACK", fg="White", command=lambda: self.back_btn_clicked())
        backbtn.grid(row=8, column=2, sticky='NSEW', padx=10, pady=10)

    def saveAdmin_btn_clicked(self):
        """This methods is the last to be call it saves the student in the database"""
        mat = self.var_txt_mat.get()
        name = self.var_txt_name.get()
        lname = self.var_txt_lname.get()
        level = self.var_txt_level.get()
        spec = self.var_txt_spec.get()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO Etudiant (matricule_etud, nom, prenom, niveau, specialite, id_reconn) VALUES \
                        (%s, %s, %s, %s, %s, %s)"
                try:
                    with open("FILES/currentReconn_ID.svr", "r") as fic:
                        id_reconn = fic.read()
                        try:
                            cursor.execute(sql, (mat, name, lname, level, spec, id_reconn,))
                        except pymysql.err.IntegrityError as e:
                            print("cannot duplicate Student : " + str(e))
                        fic.close()
                except IOError as e:
                    print("can't read FILES/currentReconn_ID.svr : " + str(e))
            # connection is not autocommit by default.So lets commit to save changes
            connection.commit()
        finally:
            pass
            # connection.close()

    def back_btn_clicked(self):
        """This methods is responsible to wipe the currents widgets and get back to the menu frame"""
        self.controller.show_frame(PageOne)

    def recon_btn_clicked(self):
        """This methods is responsible to launch the dataset creator"""
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT COUNT(*) FROM Etudiant"
                cursor.execute(sql,)
                result = cursor.fetchone()
                id_reconn = int(result['COUNT(*)']) + 1
                InputFeature.main(id_reconn)  # Launch the dataset creating process
                with open("FILES/currentReconn_ID.svr", "w") as fic:
                    fic.write(str(id_reconn))
                    fic.close()
        finally:
            pass


class RegisterAdmin(tk.Frame):
    """This class set and configure widgets to regisrter am administrator.
    ARGS :

        -   tk.Frame
        -   parent
        -   controller
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        flag = True
        self.controller = controller
        self.var_txt_mat = tk.StringVar()
        self.var_txt_name = tk.StringVar() # get Text variables
        self.var_txt_lname = tk.StringVar()
        self.var_txt_uname = tk.StringVar()
        self.var_txt_passwd = tk.StringVar()

        label = tk.Label(self, text="Enregistrer Un Administrateur", font="Arial,16")
        label.grid(row=0, column=0, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

        label_matricule = tk.Label(self, text="Matricule Admin")
        label_name = tk.Label(self, text="Nom")
        label_lastname = tk.Label(self, text="Prenom")
        label_username = tk.Label(self, text="Nom utilisateur")
        label_password = tk.Label(self, text="Mot de passe")

        entry_matricule = tk.Entry(self, textvariable=self.var_txt_mat) # entry text
        entry_name = tk.Entry(self, textvariable=self.var_txt_name)
        entry_lastname = tk.Entry(self, textvariable=self.var_txt_lname)
        entry_username = tk.Entry(self, textvariable=self.var_txt_uname)
        entry_password = tk.Entry(self, textvariable=self.var_txt_passwd)

        label_matricule.grid(row=2, column=0, sticky='NSEW', padx=10, pady=10) # position of labels
        label_name.grid(row=3, column=0, sticky='NSEW', padx=10, pady=10)
        label_lastname.grid(row=4, column=0, sticky='NSEW', padx=10, pady=10)
        label_username.grid(row=5, column=0, sticky='NSEW', padx=10, pady=10)
        label_password.grid(row=6, column=0, sticky='NSEW', padx=10, pady=10)

        entry_matricule.grid(row=2, column=1, sticky='NSEW', padx=10, pady=10) # position of entry text
        entry_name.grid(row=3, column=1, sticky='NSEW', padx=10, pady=10)
        entry_lastname.grid(row=4, column=1, sticky='NSEW', padx=10, pady=10)
        entry_username.grid(row=5, column=1, sticky='NSEW', padx=10, pady=10)
        entry_password.grid(row=6, column=1, sticky='NSEW', padx=10, pady=10)

        saveStudbtn = tk.Button(self, text="Sauveguarder", bg="BlACK", fg="White", # save btn
                                command=lambda: self.saveAdmin_btn_clicked())
        saveStudbtn.grid(row=8, column=1, sticky='NSEW', padx=10, pady=10)

        backbtn = tk.Button(self, text="Retour", bg="BlACK", fg="White", command=lambda: self.back_btn_clicked())
        backbtn.grid(row=8, column=2, sticky='NSEW', padx=10, pady=10)

    def saveAdmin_btn_clicked(self):
        """This methods is the last to be call it saves the new administrator in the database"""
        mat = self.var_txt_mat.get()
        name = self.var_txt_name.get()
        lname = self.var_txt_lname.get()
        uname = self.var_txt_uname.get()
        passwd = self.var_txt_passwd.get()
        password = hashlib.sha3_512(passwd.encode()).hexdigest()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO Personnel_bepresent (id_admin, nom, prenom, nomUtilisateur, motPasse) VALUES \
                        (%s, %s, %s, %s, %s)"
                try:
                    cursor.execute(sql, (mat, name, lname, uname, password,))
                except pymysql.err.IntegrityError as e:
                    print("cannot duplicate Admin : " + str(e))
            # connection is not autocommit by default.So lets commit to save changes
            connection.commit()
        finally:
            pass
            # connection.close()

    def back_btn_clicked(self):
        """This methods is responsible to wipe the currents widgets and get back to the menu frame"""
        self.controller.show_frame(PageOne)


class RegisterDepartment(tk.Frame):
    """This class set and configure widgets to regisrter a departement.
    ARGS :

        -   tk.Frame
        -   parent
        -   controller
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        flag = True
        self.controller = controller
        self.var_txt_mat = tk.StringVar()
        self.var_txt_name = tk.StringVar()
        self.var_txt_levelNum = tk.IntVar()

        label = tk.Label(self, text="Enregistrer Un Departement", font="Arial,16")
        label.grid(row=0, column=0, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

        label_matricule = tk.Label(self, text="Code du Departement")
        label_name = tk.Label(self, text="Nom Complet")
        label_level_number = tk.Label(self, text="Nombre de Niveau") # the number of level that department can have

        entry_matricule = tk.Entry(self, textvariable=self.var_txt_mat)
        entry_name = tk.Entry(self, textvariable=self.var_txt_name)
        entry_level_number = tk.Entry(self, textvariable=self.var_txt_levelNum)

        label_matricule.grid(row=2, column=0, sticky='NSEW', padx=10, pady=10)
        label_name.grid(row=3, column=0, sticky='NSEW', padx=10, pady=10)
        label_level_number.grid(row=4, column=0, sticky='NSEW', padx=10, pady=10)

        entry_matricule.grid(row=2, column=1, sticky='NSEW', padx=10, pady=10)
        entry_name.grid(row=3, column=1, sticky='NSEW', padx=10, pady=10)
        entry_level_number.grid(row=4, column=1, sticky='NSEW', padx=10, pady=10)

        saveStudbtn = tk.Button(self, text="Sauveguarder", bg="BlACK", fg="White",
                                command=lambda: self.saveDepart_btn_clicked())
        saveStudbtn.grid(row=8, column=1, sticky='NSEW', padx=10, pady=10)

        backbtn = tk.Button(self, text="Retour", bg="BlACK", fg="White", command=lambda: self.back_btn_clicked())
        backbtn.grid(row=8, column=2, sticky='NSEW', padx=10, pady=10)

    def saveDepart_btn_clicked(self):
        """This methods is the last to be call it saves the new department in the database"""
        mat = self.var_txt_mat.get()
        name = self.var_txt_name.get()
        levelNumber = self.var_txt_levelNum.get()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO Departement_spec (code_depart, nom, nombre_niveau) VALUES \
                        (%s, %s, %s)"
                try:
                    cursor.execute(sql, (mat, name, levelNumber,))
                except pymysql.err.IntegrityError as e:
                    print("cannot duplicate Department : " + str(e))
            # connection is not autocommit by default.So lets commit to save changes
            connection.commit()
        finally:
            pass
            # connection.close()


    def back_btn_clicked(self):
        """This methods is responsible to wipe the currents widgets and get back to the menu frame"""
        self.controller.show_frame(PageOne)


class RegisterClassrooms(tk.Frame):
    """This class set and configure widgets to regisrter a classroom.
    ARGS :

        -   tk.Frame
        -   parent
        -   controller
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        flag = True
        self.controller = controller
        self.var_txt_mat = tk.StringVar() # this var represent identifier for all the tables
        self.var_txt_rasp_mac_Adress = tk.StringVar()

        label = tk.Label(self, text="Enregistrer Une Salle", font="Arial,16")
        label.grid(row=0, column=0, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

        label_matricule = tk.Label(self, text="Identifiant Salle ex: AMPHI1")
        label_rasp_mac_Adress = tk.Label(self, text="Addresse Mac Raspberry")

        entry_matricule = tk.Entry(self, textvariable=self.var_txt_mat)
        entry_rasp_mac_Adress = tk.Entry(self, textvariable=self.var_txt_rasp_mac_Adress)

        label_matricule.grid(row=2, column=0, sticky='NSEW', padx=10, pady=10)
        label_rasp_mac_Adress.grid(row=3, column=0, sticky='NSEW', padx=10, pady=10)

        entry_matricule.grid(row=2, column=1, sticky='NSEW', padx=10, pady=10)
        entry_rasp_mac_Adress.grid(row=3, column=1, sticky='NSEW', padx=10, pady=10)

        saveStudbtn = tk.Button(self, text="Sauveguarder", bg="BlACK", fg="White",
                                command=lambda: self.saveClass_btn_clicked())
        saveStudbtn.grid(row=8, column=1, sticky='NSEW', padx=10, pady=10)

        backbtn = tk.Button(self, text="Retour", bg="BlACK", fg="White", command=lambda: self.back_btn_clicked())
        backbtn.grid(row=8, column=2, sticky='NSEW', padx=10, pady=10)

    def saveClass_btn_clicked(self):
        """This methods is the last to be call it saves the classroom in the database"""
        mat = self.var_txt_mat.get()
        macAdressRasp = self.var_txt_rasp_mac_Adress.get()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO Salle (id_salle, id_raspberry) VALUES \
                        (%s, %s)"
                try:
                    cursor.execute(sql, (mat, macAdressRasp,))
                except pymysql.err.IntegrityError as e:
                    print("cannot duplicate Classrooms : " + str(e))
            # connection is not autocommit by default.So lets commit to save changes
            connection.commit()
        finally:
            pass
            # connection.close()

    def back_btn_clicked(self):
        """This methods is responsible to wipe the currents widgets and get back to the menu frame"""
        self.controller.show_frame(PageOne)


class RegisterLevels(tk.Frame):
    """This class set and configure widgets to regisrter a scchool levels.
    ARGS :

        -   tk.Frame
        -   parent
        -   controller
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        flag = True
        self.controller = controller
        self.var_txt_mat = tk.StringVar()
        self.var_txt_studNum = tk.IntVar()
        self.var_txt_spec = tk.StringVar()

        label = tk.Label(self, text="Enregistrer Un Niveau D'Etude", font="Arial,16")
        label.grid(row=0, column=0, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

        label_matricule = tk.Label(self, text="Code du Niveau ex: GI1")
        label_stud_number = tk.Label(self, text="Nombre D'Etudiants")
        label_speciality = tk.Label(self, text="Nom de la Specialite")

        entry_matricule = tk.Entry(self, textvariable=self.var_txt_mat)
        entry_stud_number = tk.Entry(self, textvariable=self.var_txt_studNum)
        entry_speciality = tk.Entry(self, textvariable=self.var_txt_spec)

        label_matricule.grid(row=2, column=0, sticky='NSEW', padx=10, pady=10)
        label_stud_number.grid(row=3, column=0, sticky='NSEW', padx=10, pady=10)
        label_speciality.grid(row=4, column=0, sticky='NSEW', padx=10, pady=10)

        entry_matricule.grid(row=2, column=1, sticky='NSEW', padx=10, pady=10)
        entry_stud_number.grid(row=3, column=1, sticky='NSEW', padx=10, pady=10)
        entry_speciality.grid(row=4, column=1, sticky='NSEW', padx=10, pady=10)

        saveStudbtn = tk.Button(self, text="Sauveguarder", bg="BlACK", fg="White",
                                command=lambda: self.saveLevels_btn_clicked())
        saveStudbtn.grid(row=8, column=1, sticky='NSEW', padx=10, pady=10)

        backbtn = tk.Button(self, text="Retour", bg="BlACK", fg="White", command=lambda: self.back_btn_clicked())
        backbtn.grid(row=8, column=2, sticky='NSEW', padx=10, pady=10)

    def saveLevels_btn_clicked(self):
        """This methods is the last to be call it saves the levels in the database"""
        mat = self.var_txt_mat.get()
        student_number = self.var_txt_studNum.get()
        spec = self.var_txt_spec.get()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO Niveau (code_niveau, nombre_etud, nom_specialite) VALUES \
                        (%s, %s, %s)"
                try:
                    cursor.execute(sql, (mat, student_number, spec,))
                except pymysql.err.IntegrityError as e:
                    print("cannot duplicate Study Levels : " + str(e))
            # connection is not autocommit by default.So lets commit to save changes
            connection.commit()
        finally:
            pass
            # connection.close()

    def back_btn_clicked(self):
        """This methods is responsible to wipe the currents widgets and get back to the menu frame"""
        self.controller.show_frame(PageOne)


class RegisterTeachers(tk.Frame):
    """This class set and configure widgets to regisrter a scchool teachers.
    ARGS :

        -   tk.Frame
        -   parent
        -   controller
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        flag = True
        self.controller = controller
        self.var_txt_mat = tk.StringVar()
        self.var_txt_name = tk.StringVar() # get Text variables
        self.var_txt_lname = tk.StringVar()
        self.var_txt_uname = tk.StringVar()
        self.var_txt_passwd = tk.StringVar()

        label = tk.Label(self, text="Enregistrer Un Enseignant", font="Arial,16")
        label.grid(row=0, column=0, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

        label_matricule = tk.Label(self, text="Matricule un Enseignant")
        label_name = tk.Label(self, text="Nom")
        label_lastname = tk.Label(self, text="Prenom")
        label_username = tk.Label(self, text="Nom Utilisateur ou Email")
        label_password = tk.Label(self, text="Mot de passe")

        entry_matricule = tk.Entry(self, textvariable=self.var_txt_mat) # entry text
        entry_name = tk.Entry(self, textvariable=self.var_txt_name)
        entry_lastname = tk.Entry(self, textvariable=self.var_txt_lname)
        entry_username = tk.Entry(self, textvariable=self.var_txt_uname)
        entry_password = tk.Entry(self, textvariable=self.var_txt_passwd)

        label_matricule.grid(row=2, column=0, sticky='NSEW', padx=10, pady=10)
        label_name.grid(row=3, column=0, sticky='NSEW', padx=10, pady=10)
        label_lastname.grid(row=4, column=0, sticky='NSEW', padx=10, pady=10)
        label_username.grid(row=5, column=0, sticky='NSEW', padx=10, pady=10)
        label_password.grid(row=6, column=0, sticky='NSEW', padx=10, pady=10)

        entry_matricule.grid(row=2, column=1, sticky='NSEW', padx=10, pady=10)
        entry_name.grid(row=3, column=1, sticky='NSEW', padx=10, pady=10)
        entry_lastname.grid(row=4, column=1, sticky='NSEW', padx=10, pady=10)
        entry_username.grid(row=5, column=1, sticky='NSEW', padx=10, pady=10)
        entry_password.grid(row=6, column=1, sticky='NSEW', padx=10, pady=10)

        saveStudbtn = tk.Button(self, text="Sauveguarder", bg="BlACK", fg="White",
                                command=lambda: self.saveTeachers_btn_clicked())
        saveStudbtn.grid(row=8, column=1, sticky='NSEW', padx=10, pady=10)

        backbtn = tk.Button(self, text="Retour", bg="BlACK", fg="White", command=lambda: self.back_btn_clicked())
        backbtn.grid(row=8, column=2, sticky='NSEW', padx=10, pady=10)

    def saveTeachers_btn_clicked(self):
        """This methods is the last to be call it saves the teachers in the database"""
        mat = self.var_txt_mat.get()
        name = self.var_txt_name.get()
        lname = self.var_txt_lname.get()
        uname = self.var_txt_uname.get()
        passwd = self.var_txt_passwd.get()
        password = hashlib.sha3_512(passwd.encode()).hexdigest()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO Enseignant (id_enseignant, nom, prenom, adresse_email, mot_passe) VALUES \
                                (%s, %s, %s, %s, %s)"
                try:
                    cursor.execute(sql, (mat, name, lname, uname, password,))
                except pymysql.err.IntegrityError as e:
                    print("cannot duplicate Teachers : " + str(e))
            # connection is not autocommit by default.So lets commit to save changes
            connection.commit()
        finally:
            pass
            # connection.close()

    def back_btn_clicked(self):
        """This methods is responsible to wipe the currents widgets and get back to the menu frame"""
        self.controller.show_frame(PageOne)


class RegisterCourses(tk.Frame):
    """This class set and configure widgets to regisrter a scchool teaching courses.
    ARGS :

        -   tk.Frame
        -   parent
        -   controller
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        flag = True
        self.controller = controller
        self.var_txt_mat = tk.StringVar()
        self.var_txt_name = tk.StringVar()  # get Text variables

        label = tk.Label(self, text="Enregistrer Une Matiere", font="Arial,16")
        label.grid(row=0, column=0, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

        label_matricule = tk.Label(self, text="Code matiere ex: ANGL")
        label_course_name = tk.Label(self, text="Nom matiere")

        entry_matricule = tk.Entry(self, textvariable=self.var_txt_mat)
        entry_course_name = tk.Entry(self, textvariable=self.var_txt_name)

        label_matricule.grid(row=2, column=0, sticky='NSEW', padx=10, pady=10)
        label_course_name.grid(row=3, column=0, sticky='NSEW', padx=10, pady=10)

        entry_matricule.grid(row=2, column=1, sticky='NSEW', padx=10, pady=10)
        entry_course_name.grid(row=3, column=1, sticky='NSEW', padx=10, pady=10)

        saveStudbtn = tk.Button(self, text="Sauveguarder", bg="BlACK", fg="White",
                                command=lambda: self.saveCourse_btn_clicked())
        saveStudbtn.grid(row=8, column=1, sticky='NSEW', padx=10, pady=10)

        backbtn = tk.Button(self, text="Retour", bg="BlACK", fg="White", command=lambda: self.back_btn_clicked())
        backbtn.grid(row=8, column=2, sticky='NSEW', padx=10, pady=10)

    def saveCourse_btn_clicked(self):
        """This methods is the last to be call it saves the courses in the database"""
        mat = self.var_txt_mat.get()
        course_name = self.var_txt_name.get()

        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO Matiere (code_mat, nom_mat) VALUES \
                                (%s, %s)"
                try:
                    cursor.execute(sql, (mat, course_name,))
                except pymysql.err.IntegrityError as e:
                    print("cannot duplicate Courses : " + str(e))
            # connection is not autocommit by default.So lets commit to save changes
            connection.commit()
        finally:
            pass
            # connection.close()

    def back_btn_clicked(self):
        """This methods is responsible to wipe the currents widgets and get back to the menu frame"""
        self.controller.show_frame(PageOne)


app = Page()
app.mainloop()



