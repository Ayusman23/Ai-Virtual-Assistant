import cv2
import numpy as np
from PIL import Image
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))

SAMPLES_PATH = os.path.join(os.getcwd(), 'Datasets') 
CASCADE_PATH = os.path.join(os.path.dirname(BASE_DIR), 'auth', 'haarcascade_frontalface_default.xml')
TRAINER_PATH = os.path.join(os.path.dirname(BASE_DIR), 'auth', 'trainer', 'trainer.yml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
if not os.path.exists(CASCADE_PATH):
    print(f"Error: Haar Cascade file not found at {CASCADE_PATH}")
    sys.exit()
detector = cv2.CascadeClassifier(CASCADE_PATH)

def Images_And_Labels(path):
    if not os.path.isdir(path):
        print(f"Error: Samples directory not found at {path}")
        return [], []
        
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(('.jpg', '.png'))] 
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        gray_img = Image.open(imagePath).convert('L') 
        img_arr = np.array(gray_img, 'uint8') 

        try:
            id = int(os.path.split(imagePath)[-1].split(".")[1])
        except (IndexError, ValueError):
            continue

        faces = detector.detectMultiScale(img_arr) 

        for (x, y, w, h) in faces:
            faceSamples.append(img_arr[y:y+h, x:x+w])
            ids.append(id)

    return faceSamples, ids

print("Training faces. It will take a few seconds. Wait ...")

faces, ids = Images_And_Labels(SAMPLES_PATH)

if not faces:
    print("Training failed. No faces were found or processed.")
else:
    recognizer.train(faces, np.array(ids))

    os.makedirs(os.path.dirname(TRAINER_PATH), exist_ok=True)

    recognizer.write(TRAINER_PATH)
    
    print(f"Model trained and saved to: {TRAINER_PATH}")
    print(f"Total unique IDs trained: {len(np.unique(ids))}")
    print("Now the system can recognize your face.")