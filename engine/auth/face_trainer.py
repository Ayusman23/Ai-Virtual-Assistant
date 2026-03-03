import cv2
import numpy as np
from PIL import Image
import os
import eel

def capture_samples(face_id=1):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)
    
    cascade_path = os.path.join("engine", "auth", "haarcascade_frontalface_default.xml")
    detector = cv2.CascadeClassifier(cascade_path)
    
    samples_dir = os.path.join("engine", "auth", "samples")
    os.makedirs(samples_dir, exist_ok=True)
    
    count = 0
    while True:
        ret, img = cam.read()
        if not ret: break
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            count += 1
            sample_file = os.path.join(samples_dir, f"face.{face_id}.{count}.jpg")
            cv2.imwrite(sample_file, gray[y:y+h,x:x+w])
            cv2.imshow('Face Training - Look at Camera', img)

        if cv2.waitKey(100) & 0xff == 27: break
        elif count >= 50: break

    cam.release()
    cv2.destroyAllWindows()
    return count

def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    cascade_path = os.path.join("engine", "auth", "haarcascade_frontalface_default.xml")
    detector = cv2.CascadeClassifier(cascade_path)
    
    samples_path = os.path.join("engine", "auth", "samples")
    trainer_path = os.path.join("engine", "auth", "trainer", "trainer.yml")
    os.makedirs(os.path.dirname(trainer_path), exist_ok=True)
    
    if not os.path.exists(samples_path): return False
    
    imagePaths = [os.path.join(samples_path, f) for f in os.listdir(samples_path) if f.endswith(('.jpg', '.png'))]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        gray_img = Image.open(imagePath).convert('L')
        img_arr = np.array(gray_img, 'uint8')
        try:
            id = int(os.path.split(imagePath)[-1].split(".")[1])
        except: continue

        faces = detector.detectMultiScale(img_arr)
        for (x, y, w, h) in faces:
            faceSamples.append(img_arr[y:y+h, x:x+w])
            ids.append(id)

    if not faceSamples: return False
    
    recognizer.train(faceSamples, np.array(ids))
    recognizer.write(trainer_path)
    return True
