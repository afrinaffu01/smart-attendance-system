# Smart Attendance System

An AI-based Smart Attendance System developed using Python, OpenCV, Face Recognition, and Flask to automate student attendance tracking.

## Project Overview

The Smart Attendance System uses facial recognition through a webcam to identify registered students and automatically record their attendance.

The system can classify attendance as **Present, Late, or Absent** based on the configured time and provides voice notifications to recognized students.

## Features

- Face detection and recognition
- Automatic attendance marking
- Present, Late, and Absent status
- Webcam-based attendance
- Voice notifications using text-to-speech
- Attendance records stored in CSV format
- Attendance report generation
- Attendance percentage calculation
- Flask-based web interface

## Technologies Used

- Python
- Flask
- OpenCV
- Face Recognition
- Pandas
- Pyttsx3
- HTML
- CSS
- JavaScript

## Project Structure

```text
smart-attendance-system/
├── static/
├── templates/
├── app.py
├── recognize_faces.py
├── train_faces.py
├── requirements.txt
└── README.md
```

## How It Works

1. Student face images are used to create face encodings.
2. The webcam captures the student's face.
3. The system compares the detected face with stored face encodings.
4. When a student is recognized, attendance is recorded automatically.
5. The system determines the attendance status based on the configured time.
6. A voice notification is provided to the student.
7. Attendance information can be viewed through the report interface.

## Attendance Status

- **Present** – Student is recognized within the configured attendance time.
- **Late** – Student is recognized after the present time but within the late period.
- **Absent** – Student is recognized after the configured late period.

## Installation

Clone the repository:

```bash
git clone https://github.com/afrinaffu01/smart-attendance-system.git
cd smart-attendance-system
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

## Privacy Notice

This public repository does not include real student face images, personal student information, attendance records, or private credentials.

Demo data should be used when testing the project.

## Future Improvements

- Admin dashboard
- Student login
- Database integration
- Cloud-based attendance storage
- Excel report generation
- Attendance analytics
- Improved authentication and security
- Mobile-friendly interface

## Author

**Afrin R**

B.Sc. Computer Science

GitHub: https://github.com/afrinaffu01
