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

    IMPORTS :
        -   shlex
        -   subprocess
        -   client
        -   time


    FUNCTIONS :
        -   reconnaitre()

        -   finReconn()

        -   verifier()

        -   assure_path_exists(path)


    CLASSES :

        -   SaveStudent :
                METHODS :
                    -   __init__(self, matricule_etud, nom, prenom, niveau, specialite)
                    -   send_student_informations(self)
                    -   send_images(self)

        -   ImproveRecognition :
                METHODS :
                    -    __init__(self)
                    -   send_news_images(self)

        -   StorePresences :
                METHODS :
                    -    __init__(self, teacher_id, matiere, salle, id_specialite, ID_lines)
                    -   send_news_images(self)
                    -   send_a_presence(self)
"""

import shlex, subprocess
import client
import time


class SaveStudent:
    """Class that Sends student information to the Server"""

    def __init__(self, matricule_etud, nom, prenom, niveau, specialite):
        self.matricule_etud = matricule_etud
        self.nom = nom
        self.prenom = prenom
        self.niveau = niveau
        self.spec = specialite

    def send_student_informations(self):
        student_info = "receivestudinfo:" + self.matricule_etud + "|" + self.nom + "|" + self.prenom + "|" + self.niveau + "|" + self.spec
        # '|' is the seprator of arguments
        client.socket_bind_connect()
        client.socket_send_recv(student_info)
        self.send_images()

    def send_images(self):
        client.socket_bind_connect()
        client.socket_send_recv("receiveImages")
        time.sleep(3)
        command_line = "python send_dataset.py"
        args = shlex.split(command_line)
        p = subprocess.Popen(args, shell=False)


# TODO : implement this class
class ImproveRecognition:
    """Class that send send new images of students to improve recognition"""

    def __init__(self):
        pass

    def send_news_images(self):
        # TODO : send images for a specific student
        client.socket_bind_connect()
        client.socket_send_recv("receiveImages")
        time.sleep(3)
        command_line = "python send_dataset.py"
        args = shlex.split(command_line)
        p = subprocess.Popen(args, shell=False)


class StorePresences:
    """Class that send analytics data to the server about the presence of students"""

    def __init__(self, teacher_id, matiere, salle, id_specialite, ID_lines):
        self.teacher_id = teacher_id
        self.mat = matiere
        self.salle = salle
        self.spec = id_specialite
        self.IDs = list()
        for v in ID_lines:
            arr = v.split('\n')
            if arr[0] != '':
                self.IDs.append(arr[0])
            else:
                continue
        self.IDs = list(set(self.IDs))
        self.dum = ""
        for v in self.IDs:
            self.dum = v + "-" + self.dum

    def send_a_presence(self):
        im_present = "receiveapresence:" + self.teacher_id + "|" \
                     + self.mat + "|" + self.salle + "|" + self.spec + "|" + str(self.dum)
        client.socket_bind_connect()
        client.socket_send_recv(im_present)


if __name__ == "__main__":
    s_t = StorePresences("1", "ENSEIG-1", "C", "AMPHI1", "GI")
    s_t.send_a_presence()
