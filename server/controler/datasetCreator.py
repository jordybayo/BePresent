# -*- encoding:utf-8 -*-
####################################################


# importation de opencv pour la capture de dataset ou donnee entrente(DeepLearning)
import cv2
import os
from controler.trainer import entrainer  # contoler after because this module will be call from yhe main.py Tkinter mod


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


# Commencer a capturer les images
vid_cam = cv2.VideoCapture(1)

# lecture du haarcascade respossable de la detection facial
face_detector = cv2.CascadeClassifier('controler/haar/haarcascade_frontalface_default.xml')

assure_path_exists("controler/dataset/")

# Inialiser les labels
count = 1
fin = count + 100


def apprendre(count, face_id):
    """This function is in charge to capture all face img or feed or feature that we need for the training"""
    while True:

        # Capturer un Frame d'image
        _, image_frame = vid_cam.read()

        # Convertir le frame en BGR
        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

        # Detect frames of different sizes, list of faces rectangles
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

        for (x, y, w, h) in faces:
            # utiliser le frame d'image pour dessiner le rectangle
            cv2.rectangle(image_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Incrementer le label
            count += 1

            # Sauveguarder le frame dans le fichier dataset
            cv2.imwrite("controler/dataset/Stud." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

            # Afficher le frame de video dans une video
            cv2.imshow('frame', image_frame)

        # quitter avant 100ms
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

        # Si les images prise  atteignent 100
        elif count > fin:
            break
    return True


def finApprentissage():
    """Power off the Camera and destroy opencv Window"""
    # Arretez le video
    vid_cam.release()

    # Arretez toutes les fenetres
    cv2.destroyAllWindows()


def main(face_id):
    """Launch the Dataset creating process"""
    if apprendre(count, face_id):
        entrainer()
    finApprentissage()


if __name__ == '__main__':
    latest_face_ID_plus_One = 1
    main(latest_face_ID_plus_One)
