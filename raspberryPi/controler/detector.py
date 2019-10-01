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
        -   Opencv cv2
        -   Time
        -   OS


    FUNCTIONS :
        -   reconnaitre()

        -   finReconn()

        -   verifier()

        -   assure_path_exists(path)


    MATERIALS REQUIREMENTS :

        -   Required Camera plugin and permission to use.
"""


# importation de opencv pour
import cv2
import time
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


# cree un pattern opencv pour la la reconnaissance source : Documentation
recognizer = cv2.face.LBPHFaceRecognizer_create()

#assure_path_exists("controler/trainer/")

# lecture du fichier d'entrainement
recognizer.read('controler/trainer/trainer.yml')

# lecture du haarcascade respossable de la detection facial
cascadePath = "controler/haar/haarcascade_frontalface_default.xml"

# classification d'image. je pouvais tout aussi mettre
faceCascade = cv2.CascadeClassifier(cascadePath);

# initialisatiion de la police d'ecriture
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialisation de la capture d'ecran
cam = cv2.VideoCapture(0)

# Prendre le temps de debut
debut = time.time()


def reconnaitre():
    """ Functions responsible to ::
                - Open the camera
                - Identified faces in the frame
                - draw a rectangle on each face
                - determine a confidence

        PARAMETERS :
            -

        RETURNS :
            -  confidence . Type: Double
                # The confidence is DeepLearning that permit us to judge the prediction
    """
    while True:
        # lecture de la camera
        ret, im = cam.read()

        # Convertion des frames RVB en BGR/gris pour que opencv puise les traiter
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        # Recuperation des faces
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

        # pour toutes les faces
        for (x, y, w, h) in faces:

            # rectangle Identificateur de face
            cv2.rectangle(im, (x, y), (x+w, y+h), (222,245,160), 2)

            # reconnaissance de la face qui correspond a L' ID enregistrer
            Id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            if not confidence >= 50:
                name = "People-F: {0:.2f}%".format(round(100 - confidence, 2))
                color = (250, 149, 23)
                stroke = 4
                cv2.putText(im, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            elif confidence >= 50:
                name = "{0:.2f}%".format(round(100 - confidence, 2))
                color = (0, 255, 0)
                stroke = 4
                cv2.putText(im, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
                return "{0:.2f}".format(round(120 - confidence, 2)), Id
        # affichage de la video dans la fenetre opencv
        cv2.imshow('im', im)

        # arreter a si pression sur K
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


def finReconn():
    """ Functions responsible to Stop face recognition and end videocapture

        PARAMETERS :
            -

        RETURNS :
            -
    """
    # Arretez la camera
    cam.release()

    # Close all windows
    cv2.destroyAllWindows()


def verifier():
    """ Functions responsible to ::
                - set the a timer
                - look for time each microseconds
                - verify if time set to recognition is obtain
                - then launch the stop recognition function (finReconn)

        PARAMETERS :
            -

        RETURNS :
            -  True/False . Type: Bool
                # This permit us to says that time of recognition is finish and was successfull
    """
    global debut
    fin = time.time()
    timer_counter = fin - debut
    while int(timer_counter) < 10:
        var, id = reconnaitre()  # Id pour identifier de maniere unique chaque etudiant

        var = float(var)
        fin = time.time()
        timer_counter = fin - debut
        print("temps= " + str(timer_counter))

        if var >= 50.0:
            print("Identifie " + str(var))
            with open("controler/Ids/currentIds.txt", "a") as fic:
                fic.write("\n" + str(id))
                fic.close()
        else:
            print("Non Identification ! " + str(var))


if __name__ == '__main__':
    verifier()