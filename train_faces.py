import face_recognition
import os
import pickle

dataset = "dataset"

known_faces = []
known_names = []

for person in os.listdir(dataset):

    person_folder = os.path.join(dataset, person)

    for image in os.listdir(person_folder):

        img_path = os.path.join(person_folder, image)

        img = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(img)

        if len(encodings) > 0:

            known_faces.append(encodings[0])
            known_names.append(person)

data = {"encodings": known_faces, "names": known_names}

with open("faces.pickle", "wb") as f:
    pickle.dump(data, f)

print("Face training completed successfully")