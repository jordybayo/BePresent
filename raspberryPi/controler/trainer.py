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
"""A Face recognition Module based on Opencv .

    IMPORTS :
        -   Opencv or cv2


    FUNCTIONS :
        -   assure_path_exists(path)

        -   getImagesAndLabels(path)

        -   entrainer()

"""

# Import OpenCV2 for image processing
# Import os for file path
import cv2

# Import numpy for matrix calculation
import numpy as np

# Import Python Image Library (PIL)
from PIL import Image

import os


def assure_path_exists(path):
    """ Functions responsible to verify if the path exist really

        ARGS :
            - path . Type:String

        RETURNS :
            -
    """
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


# Create Local Binary Patterns Histograms for face recognization
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Using prebuilt frontal face training model, for face detection
detector = cv2.CascadeClassifier("controler/haar/haarcascade_frontalface_default.xml")


# Create method to get the images and label data
def getImagesAndLabels(path):
    """ Functions responsible to  ::
                - Open each photo
                - Identified faces in the frame
                - manage IDs

        ARGS :
            - path . Type:String

        RETURNS :
            - (faceSamples, ids) . Type: Tuple
    """
    # Get all file path
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    # Initialize empty face sample
    faceSamples = []

    # Initialize empty id
    ids = []

    # Loop all the file path
    for imagePath in imagePaths:

        # Get the image and convert it to grayscale
        PIL_img = Image.open(imagePath).convert('L')

        # PIL image to numpy array
        img_numpy = np.array(PIL_img, 'uint8')

        # Get the image id
        id = int(os.path.split(imagePath)[-1].split(".")[1])

        # Get the face from the training images
        faces = detector.detectMultiScale(img_numpy)

        # Loop for each face, append to their respective ID
        for (x, y, w, h) in faces:
            # Add the image to face samples
            faceSamples.append(img_numpy[y:y + h, x:x + w])

            # Add the ID to IDs
            ids.append(id)

    # Pass the face array and IDs array
    return faceSamples, ids


def entrainer():
    """ Functions responsible to take all the images in the path
        and train them with unique Ids for a future train then save
        the trainngs in the .yaml trainer file

        ARGS :
            - path . Type:String

        RETURNS :
            - (faceSamples, ids) . Type: Tuple
    """
    # Get the faces and IDs
    faces, ids = getImagesAndLabels('controler/dataset')

    # Train the model using the faces and IDs
    recognizer.train(faces, np.array(ids))  # training began

    # Save the model into trainer.yml
    assure_path_exists('controler/trainer/')
    recognizer.save('controler/trainer/trainer.yml')