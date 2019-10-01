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
"""A multiple connection server sender and receiver .

    IMPORTS :
        -  com2raspberry


    FUNCTIONS :
        -   create_socket()

        -   bind_socket()

        -   socket_accept()

        -  send_command(conn, msg)

        -   main()


    MATERIALS REQUIREMENTS :

        -   Required Server port not in usage.
"""

import socket
import threading
import time
import select
import com2raspberry
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='bepresent_pers',
                             password='password',
                             db='bepresent',
                             port=3306,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor
                             )
host = ""
port = 12800
s = None
CLIENT_IP = list()
all_connection = list()
my_lock = threading.RLock()


# create a socket(connect two computer)
def create_socket():
    try:
        global host
        global port
        global s  # socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Socket exception error:" + str(msg))


# binding the socket and listenning for connexion
def bind_socket():
    """set all the parameters needed to bind the socket"""
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
    """socket accept is a multithreading and async function type that can allow many device to connect to server"""
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
            # send_command("yoyo")


# send commad to the client/victim or a friend
def send_command(conn, msg):
    """The sender function send a message that he've encode in bytes type to be transfer on the network"""
    msg2send = msg.encode()
    conn.send(msg2send)


def receive_command():
    """The receiver command receive bytes data decode them and send them to the interpreter to analyse"""
    global all_connection
    with my_lock:
        for conn in all_connection:
            msg_recu = conn.recv(1024)
            msg = msg_recu.decode()
            print(msg)
            interpreter(conn, msg)


def interpreter(conn, msg):
    """The methods is able to recognize the client device(raspberry Pi or phone) and answer to his request"""
    arr = msg.split(":")  # the message contain something like that "rasp:message"
    if (arr[0] == "rasp") and (arr[1] == "receiveImages"):
        execution = com2raspberry.SaveStudent()
        execution.recv_images()
        send_command(conn, "end")  # when images have been received close connection
        quit_gracefully(conn)

    elif (arr[0] == "rasp") and (arr[1] == "receivestudinfo"):
        arrStInfo = arr[2].split("|")  # the third part contains student information
        execution = com2raspberry.SaveStudent(arrStInfo[0], arrStInfo[1], arrStInfo[2], arrStInfo[3], arrStInfo[4])
        execution.store_stud_info()
        send_command(conn, "end")
        quit_gracefully(conn)

    elif (arr[0] == "rasp") and (arr[1] == "receiveapresence"):
        arrStInfo = arr[2].split("|")  # the third part contains students IDs and teacher Info
        ID_list = arrStInfo[4].split("-")
        studsName = list()  # this list contains all the names of students present #
        print("ID_list = " + str(ID_list))
        for v in ID_list:
            # Get the name of each ID to send back to the rasp that will send to the phone
            if v != '' and v != '\n':
                print("la valeur de V:" + str(v))
                try:
                    with connection.cursor() as cursor:
                        # Read a single record
                        sql = "SELECT nom,prenom FROM Etudiant WHERE id_reconn=%s"
                        cursor.execute(sql, (v,))
                        result = cursor.fetchone()
                        studsName.append(str(result["nom"]) + " " + str(result["prenom"]))
                    # connection is not autocommit by default.So lets commit to save changes
                    connection.commit()
                finally:
                    pass

                execution = com2raspberry.StorePresences(v, arrStInfo[0], arrStInfo[1], arrStInfo[2], arrStInfo[3])
                execution.recv_a_presence()
        resultBack = "|"
        for v in studsName:
            resultBack = v + resultBack
        resultBack = "end:" + resultBack
        send_command(conn, resultBack)  # send the results back to the teacher
        quit_gracefully(conn)
    else:
        print("unknow device !!")


def quit_gracefully(conn):
    """close a specific client connection(conn)"""
    conn.close()
    object_2_delete = all_connection.index(conn)
    del all_connection[object_2_delete]


def main():
    global all_connection
    global s
    create_socket()
    bind_socket()
    socket_accept()

    for clients in all_connection:
        clients.close()
    s.close()


if __name__ == '__main__':
    main()
