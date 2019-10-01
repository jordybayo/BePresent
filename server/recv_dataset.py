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
"""A tcp/ftp Client Module that receives images rom an tcp/ftp server.

    FUNCTIONS :
        -

    MATERIALS REQUIREMENTS :

        -   Required client port not in use and sever ready.
"""

import socket
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
cursor = connection.cursor()
identifier = cursor.execute("SELECT * FROM Etudiant")

serversock = socket.socket()
host = ''
port = 12801
serversock.bind((host, port))
filename = ""
serversock.listen(10)
print("Waiting for a connection.....")

clientsocket, addr = serversock.accept()
print("Got a connection from %s" % str(addr))
while True:
    size = clientsocket.recv(16)  # Note that you limit your filename length to 255 bytes.
    if not size:
        break
    size = int(size, 2)
    filename = clientsocket.recv(size)
    filename = "controler/dataset/Stud." + str(identifier) + "." + str(filename.decode())
    filesize = clientsocket.recv(32)
    filesize = int(filesize, 2)
    file_to_write = open(filename, 'wb')
    chunksize = 4096
    while filesize > 0:
        if filesize < chunksize:
            chunksize = filesize
        data = clientsocket.recv(chunksize)
        file_to_write.write(data)
        filesize -= len(data)

    file_to_write.close()
    print('File received successfully')
serversock.close()
