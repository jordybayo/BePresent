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
"""A Client code that send an image dataset to the server .

    IMPORTS :
        -   socket
        -   os


    FUNCTIONS :
        -
"""

import socket
import os

s = socket.socket()
host = socket.gethostname()
port = 12801
s.connect((host, port))
path = "controler/tempDataset"
directory = os.listdir(path)
for files in directory:
    print (files)
    filename = files
    size = len(filename)
    size = bin(size)[2:].zfill(16) # encode filename size as 16 bit binary
    s.send(size.encode())
    s.send(filename.encode())

    filename = os.path.join(path,filename)
    filesize = os.path.getsize(filename)
    filesize = bin(filesize)[2:].zfill(32) # encode filesize as 32 bit binary
    s.send(filesize.encode())

    file_to_send = open(filename, 'rb')

    l = file_to_send.read()
    s.sendall(l)
    file_to_send.close()
    print ('File Sent')

s.close()
