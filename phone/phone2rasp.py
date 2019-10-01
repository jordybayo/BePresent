# -*-encoding:utf-8-*-

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
"""An Client sender/receiver module that communicate with raspberry to ask to launch
    presence veriffication and send back result or student present in class

    MATERIALS REQUIREMENTS :

        -   Required wifi enable and connected to the school network(IUT-FV) to run socket
            and sqlite.db to extract raspberry ip in function of the class
"""

import socket

hote = 'localhost'
port = 0
msg_a_envoyer = b""
connexion_avec_server = None

def socket_bind_connect(port_variable, hote_variable='10.42.0.145'):
    global connexion_avec_server
    global port
    global hote
    hote = hote_variable
    port = port_variable
    connexion_avec_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_avec_server.connect((hote, port))
    print("connexion etablite avec le port {}".format(port))


def socket_send_recv(msg):
    global connexion_avec_server
    global msg_a_envoyer

    msg_a_envoyer = "phone:" + str(msg)
    msg_a_envoyer = msg_a_envoyer.encode()
    connexion_avec_server.send(msg_a_envoyer)

    msg_recu = connexion_avec_server.recv(1024)
    msg_a_envoyer = msg_a_envoyer.decode()
    if msg_recu.decode() == "end":
        socket_close()
    elif msg_recu.decode() != "end":
        end_msg = str(msg_recu.decode())
        arr = end_msg.split(":")
        if arr[0] == "end":
            socket_close()
            with open("FILES/asyncwait.ph", "w") as fic:
                fic.write("0")  # switch off the loading popup
                fic.close()
            student = arr[1].split("|")
            with open("FILES/currentAttce.ph", "w") as fic:
                for stud in student:
                    fic.write("\n" + str(stud))
                fic.close()






def socket_close():
    global connexion_avec_server
    connexion_avec_server.close()
    print("fermeture de la connexion avec le serveur ...")


def main():
    socket_bind_connect()
    while True:
        socket_send_recv("bepresent is automatic")

if __name__ == '__main__':
    main()
