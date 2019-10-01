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
"""A Face recognition Module based on Opencv .

    CLASSES :
        -   SaveStudent

                METHODS :
                    -   __init__(self, matricule_etud="", nom="", prenom="", niveau="", specialite="")
                    -   store_stud_info(self)
                    -   recv_images(self)

    CLASSES :
        -   StorePresences

                METHODS :
                    -  __init__(self, recognition_id, teacher_id, matiere, id_salle, id_specialite)
                    -   recv_a_presence(self)
                    -

    FUNCTIONS :
        -   main()



    REQUIREMENTS :

        -   Require database ready and 3306 port opened .
"""


import shlex, subprocess
import pymysql.cursors
from datetime import datetime

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='bepresent_pers',
                             password='password',
                             db='bepresent',
                             port=3306,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor
                             )


class SaveStudent:
    """Class that Receive student informations and store them in the database."""

    def __init__(self, matricule_etud="", nom="", prenom="", niveau="", specialite=""):
        """variable already initilize to allow recv_images to be called without parameters"""
        self.matricule_etud = matricule_etud
        self.nom = nom
        self.prenom = prenom
        self.niveau = niveau  # because the database only take integer for this row
        self.spec = specialite

    def store_stud_info(self):
        cursor = connection.cursor()
        recog_id = cursor.execute("SELECT * FROM Etudiant")
        recog_id = recog_id + 1
        print("Recognition Id is : " + str(recog_id))
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO Etudiant (matricule_etud, nom, prenom, niveau, specialite, id_reconn) VALUES \
                        (%s, %s, %s, %s, %s, %s)"
                try:
                    cursor.execute(sql, (self.matricule_etud, self.nom, self.prenom, self.niveau, self.spec, recog_id,))
                except pymysql.err.IntegrityError as e:
                    print("cannot duplicate student : " + str(e))
            # connection is not autocommit by default.So lets commit to save changes
            connection.commit()
        finally:
            pass
            # connection.close()

    def recv_images(self):
        command_line = "python recv_dataset.py"
        args = shlex.split(command_line)
        p = subprocess.Popen(args, shell=False)


class StorePresences:
    """Class that send analytics data to the server about the presence of students"""

    def __init__(self, recognition_id, teacher_id, matiere, id_salle, id_specialite):
        self.recogn_id = recognition_id
        self.teacher_id = teacher_id
        self.mat = matiere
        self.id_salle = id_salle
        self.spec = id_specialite

    def recv_a_presence(self):
        try:
            with connection.cursor() as cursor:

                # Read a single record
                sql = "SELECT matricule_etud FROM Etudiant WHERE id_reconn=%s"
                cursor.execute(sql, (self.recogn_id,))
                result = cursor.fetchone()
                matricule_etud = str(result["matricule_etud"])

                now = datetime.now()
                fornatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

                # Create a new record
                sql = "INSERT INTO stat_presence (specialite, matricule_etud, id_enseig, id_salle, id_mat, date_heure) \
                            VALUES (%s, %s, %s, %s, %s, %s)"
                try:
                    cursor.execute(sql, (self.spec, matricule_etud, self.teacher_id, self.id_salle, self.mat, fornatted_date,))
                except pymysql.err.IntegrityError as e:
                    print("cannot duplicate student : " + str(e))
            # connection is not autocommit by default.So lets commit to save changes
            connection.commit()
        finally:
            pass
            # connection.close()


def main():
    r_t = SaveStudent()
    r_t.recv_images()


if __name__ == '__main__':
    main()
