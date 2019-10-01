# -*- encoding:utf-8 -*-

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
"""A client module that connect to the server and make to perform send/receive.

    IMPORTS :
        -   socket

    FUNCTIONS :
        -   socket_bind_connect()

        -   socket_send_recv(msg)

        -   socket_close()

        -   main()
"""

import socket

hote = 'localhost'
port = 12800
msg_a_envoyer = b""
connexion_avec_server = None

def socket_bind_connect():
    """ Functions responsible to bind connection to a specific server await

        ARGS :
            -

        RETURNS :
            -
    """
    global connexion_avec_server
    connexion_avec_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_avec_server.connect((hote, port))
    print("connexion etablite avec le port {}".format(port))


def socket_send_recv(msg):
    """ Functions responsible to receive and send data to the server that have been connected to ::
            -it encode each message to send with a the
                string 'rasp' which mean raspberry to make the server identified the sender

            - Launch the quit server connection server (socket_close())

        ARGS :
            - msg . Type:String
                This arg is the message we want to send

        RETURNS :
            -
    """
    global connexion_avec_server
    global msg_a_envoyer

    msg_a_envoyer = "rasp:" + str(msg)
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
            phoneConn = None
            with open("phoneIp.txt", "r") as fic:
                phone_Proto = fic.readline()  # parameters to connect to the phone
                phone_fileno = fic.readline()
                phoneConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM, int(phone_Proto), int(phone_fileno))
                fic.close()
            arr[1] = "end:" + arr[1]
            phoneConn.send(arr[1].encode())  # send the students attendances to the teacher's phone
            socket_close()


def socket_close():
    """ Functions responsible to quit the server connection

        ARGS :
            -

        RETURNS :
            -
    """
    global connexion_avec_server
    connexion_avec_server.close()
    print("fermeture de la connexion avec le serveur ...")


def main():
    """ Functions responsible to ::
            - bind or connect to the server connection
            - and while is True perform an await function to see if a message has been sended or send a message

        ARGS :
            -

        RETURNS :
            -
    """
    socket_bind_connect()
    while True:
        socket_send_recv("bepresent is automatic")

if __name__ == '__main__':
    main()