import cv2
import face_recognition
import pickle
from datetime import datetime
import pyttsx3
import pandas as pd
import os

# 🔊 Voice engine
engine = pyttsx3.init()

# 🔥 CHANGE TIME HERE (AM/PM FORMAT)
PRESENT_TIME = "11:00 PM"
LATE_TIME = "11:05 PM"

# 🔥 Convert string → time
def convert_to_time(time_str):
    return datetime.strptime(time_str, "%I:%M %p").time()

# Load trained faces
with open("faces.pickle", "rb") as f:
    data = pickle.load(f)

# Start camera
video = cv2.VideoCapture(0)

attendance_file = "attendance.csv"

# Create attendance file if not exists
if not os.path.exists(attendance_file):
    df = pd.DataFrame(columns=["Name", "Date", "Time", "Status"])
    df.to_csv(attendance_file, index=False)

# Avoid duplicate entries
marked_today = set()

while True:

    ret, frame = video.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, faces)

    for (top, right, bottom, left), encoding in zip(faces, encodings):

        matches = face_recognition.compare_faces(data["encodings"], encoding)
        face_distances = face_recognition.face_distance(data["encodings"], encoding)

        name = "Unknown"

        if len(face_distances) > 0:
            best_match = face_distances.argmin()

            if matches[best_match]:
                name = data["names"][best_match]

        # Draw rectangle
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Show name
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, color, 2)

        # If recognized
        if name != "Unknown":

            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            current_time_str = now.strftime("%I:%M:%S %p")

            if (name, date) not in marked_today:

                # 🔥 TIME LOGIC (AM/PM BASED)
                current_time = now.time()

                present_time = convert_to_time(PRESENT_TIME)
                late_time = convert_to_time(LATE_TIME)

                if current_time <= present_time:
                    status = "Present"
                    engine.say(f"Hello {name}, Present. Have a nice day")

                elif present_time < current_time <= late_time:
                    status = "Late"
                    engine.say(f"Hello {name}, You are late. Try to come earlier")

                else:
                    status = "Absent"
                    engine.say(f"Hello {name}, You are marked absent")

                engine.runAndWait()

                # Save attendance
                df = pd.read_csv(attendance_file)

                new_data = pd.DataFrame([[name, date, current_time_str, status]],
                                        columns=["Name", "Date", "Time", "Status"])

                df = pd.concat([df, new_data], ignore_index=True)
                df.to_csv(attendance_file, index=False)

                marked_today.add((name, date))

            # Show status
            cv2.putText(frame, status, (left, bottom + 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, color, 2)

        else:
            cv2.putText(frame, "Unknown Face", (left, bottom + 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 0, 255), 2)

    cv2.imshow("Face Attendance System", frame)

    if cv2.waitKey(1) == 27:
        break

video.release()
cv2.destroyAllWindows()