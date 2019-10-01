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
"""A raspberry pi Server module that accept phones'connections and communicate with tem.

    IMPORTS :
        -   socket
        -   threading
        -   time
        -   select
        -   com2server (project module)
        -   controler.detector as faceDetector (project module)
        -   os


    FUNCTIONS :
        -   reconnaitre()

        -   finReconn()

        -   verifier()

        -   assure_path_exists(path)

"""

import socket
import threading
import select
import com2server
from controler.detector import verifier as faceDetector
import os
import asyncio
import time
import shlex, subprocess
import time

host = ""
port = 12803
s = None
CLIENT_IP = list()
all_connection = list()
my_lock = threading.RLock()


class PingAssets(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.signal = True

    def run(self):
        while self.signal:
            faceDetector()
            time.sleep(60000)

    def OnStop(self):
            self.signal = False


# create a socket(connect two computer)
def create_socket():
    """ Functions responsible to set the global variables of connection

        ARGS :
            -

        RETURNS :
            -
    """
    try:
        global host
        global port
        global s  # socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Socket exception error:" + str(msg))


# binding the socket and listenning for connexion
def bind_socket():
    """ Functions responsible to bind raspberry server await socket

        ARGS :
            -

        RETURNS :
            -
    """
    try:
        global host
        global port
        global s
        print("Binding the port " + str(port))
        s.bind((host, port))
        s.listen(5)
        print("Bindind Done..")
    except socket.error as msg:
        print("Socket bindin Error  " + str(msg) + ".Retrying...")
        time.sleep(10)
        bind_socket()


# establish the connection with the client (socket must be listenning)
def socket_accept():
    """ Functions responsible to bind and wait for incommings connections before accept

        ARGS :
            -

        RETURNS :
            -
    """
    global all_connection
    while True:
        asked_connection, wlist, xlist = select.select([s], [], [], 0.05)
        for connexion in asked_connection:
            conn, address = connexion.accept()
            all_connection.append(conn)
            CLIENT_IP.append(address)
            print("connexion has been establish with | " + str(address) + " | IP_list:" + str(CLIENT_IP[:]))
            # #print( (CLIENT_IP[0])[1] )
            # for var in CLIENT_IP:
            #     print("mac: "+ str( get_mac_address( ip=var[0] ) ) )
        try:
            client_a_lire, wlist, xlist = select.select(all_connection, [], [], 0.05)
        except select.error:
            pass
        else:
            thr_recv = threading.Thread(target=receive_command)
            thr_recv.start()
            # send_command("")


# send commad to the client/victim or a friend
def send_command(conn, msg):
    msg2send = msg.encode()
    conn.send(msg2send)


def receive_command():
    """ Functions responsible to receive message and send it to the interpreter

        ARGS :
            -

        RETURNS :
            -
    """
    global all_connection
    with my_lock:
        for conn in all_connection:
            message = conn.recv(1024)
            msg = message.decode()
            print(msg)
            interpreter(conn, msg)


def interpreter(conn, msg):
    """ Functions responsible to ::
            - interprete the message
            - determine the sender with the flag string 'phone'

        ARGS :
            - conn . Type: socket typ
            - msg

        RETURNS :
            -
    """
    arr = msg.split(":")  # the message contain something like that "rasp:message"
    if (arr[0] == "phone") and (arr[1] == "detectStudentface"):
        try:
            os.remove("controler/Ids/currentIds.txt")
        except IOError as e:
            print("can't delete file: " + str(e))

        debut = time.time()
        fin = time.time()
        timer_counter = fin - debut
        while int(timer_counter) < 20:
            timer_counter = fin - debut
            command_line = "python controler/detector.py"
            args = shlex.split(command_line)
            p = subprocess.Popen(args, shell=False)
            fin = time.time()
            print("temps = " + str(timer_counter))

        try:
            with open("controler/Ids/currentIds.txt", "r") as fic:
                ids = fic.readlines()
                fic.close()
        except IOError as e:
            print("No ID in the File: " + str(e))

        with open("phoneIp.txt", "w") as fic:
            fic.write(str(conn.proto))  # replace the file with new conmection parameters
            fic.write("\n" + str(conn.fileno()))
            fic.close()
        arr_detect = arr[2].split("|")
        strp = com2server.StorePresences(arr_detect[1], arr_detect[2], arr_detect[0], arr_detect[3], ids)
        strp.send_a_presence()
    else:
        print("i dont know you")


def quit_gracefully(conn):
    """ Functions responsible to end connection with a client by poping it dron the list items

        ARGS :
            - conn . Type: socket type

        RETURNS :
            -
    """
    conn.close()
    object_2_delete = all_connection.index(conn)
    del all_connection[object_2_delete]


def main():
    """ Functions responsible to run all the function required to launch server

        ARGS :
            -

        RETURNS :
            -
    """
    print('Hello')
    global all_connection
    global s
    create_socket()
    bind_socket()
    socket_accept()

    for clients in all_connection:
        clients.close()
        print("Clients locked")
    s.close()


if __name__ == '__main__':
    main()
