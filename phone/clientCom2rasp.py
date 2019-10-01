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
        -   phone2rasp


    MATERIALS REQUIREMENTS :

        -   Required client port not in use and raspberry server ready.
"""

import phone2rasp
import sqlite3
connection = sqlite3.connect('bepresentteach.db')
conn = connection.cursor()


class SaveStudent:
    """Class that Sends student information to the Server
        ARGS :
            - classname
            - teacher_id
            - matiere   # course name
            - id_specialite
        """

    def __init__(self, classname, teacher_id, matiere, id_specialite):
        self.crn = classname  # classrooms names
        self.teacher_id = teacher_id
        self.mat = matiere
        self.idSpc = id_specialite

    def send_detection_starting(self):
        detect_start_msg = "detectStudentface:" + self.crn + "|" + self.teacher_id + "|" + self.mat + \
                           "|" + self.idSpc
        # ':' is the seprator of arguments
        conn.execute("SELECT raspberry_id_port,raspberry_ip FROM classconfig WHERE classroom_name = '{}'"
                     .format(self.crn.upper()))
        self.validcheck = conn.fetchone()
        connection.commit()
        port = self.validcheck[0]  # get the port from the database
        phone2rasp.socket_bind_connect(port)
        phone2rasp.socket_send_recv(detect_start_msg)


if __name__ == "__main__":
    s_t = SaveStudent("")
    s_t.send_detection_starting()
