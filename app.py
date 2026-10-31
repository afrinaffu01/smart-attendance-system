from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import subprocess
import os

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- ADMIN LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            return redirect("/dashboard")

    return render_template("login.html")


# ---------------- STUDENT FACE LOGIN ----------------
@app.route("/student")
def student():
    subprocess.Popen(["python", "recognize_faces.py"])
    return redirect("/")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    students = pd.read_csv("students.csv") if os.path.exists("students.csv") else pd.DataFrame()
    attendance = pd.read_csv("attendance.csv") if os.path.exists("attendance.csv") else pd.DataFrame()

    # Merge data
    if not attendance.empty and not students.empty:
        data = pd.merge(attendance, students, on="Name", how="left")

        # Fix columns safely
        if "RegisterNo_y" in data.columns:
            data["RegisterNo"] = data["RegisterNo_y"]

        if "Department" not in data.columns and "Department_y" in data.columns:
            data["Department"] = data["Department_y"]

    else:
        data = attendance

    # Attendance report
    if attendance.empty:
        report = pd.DataFrame()
    else:
        report = attendance.groupby("Name").agg(
            Total=("Status", "count"),
            Present=("Status", lambda x: (x == "Present").sum()),
            Late=("Status", lambda x: (x == "Late").sum())
        ).reset_index()

        report["Percentage"] = ((report["Present"] + report["Late"]) / report["Total"]) * 100

    return render_template(
        "dashboard.html",
        total_students=len(students),
        attendance=data.to_dict(orient="records"),
        report=report.to_dict(orient="records")
    )


# ---------------- DOWNLOAD EXCEL ----------------
@app.route("/download")
def download():

    if os.path.exists("attendance.csv") and os.path.exists("students.csv"):

        attendance = pd.read_csv("attendance.csv")
        students = pd.read_csv("students.csv")

        data = pd.merge(attendance, students, on="Name", how="left")

        # Fix columns
        if "RegisterNo_y" in data.columns:
            data["RegisterNo"] = data["RegisterNo_y"]

        if "Department" not in data.columns and "Department_y" in data.columns:
            data["Department"] = data["Department_y"]

        final_data = data[[
            "RegisterNo",
            "Name",
            "Department",
            "DOB",
            "Email",
            "Date",
            "Time",
            "Status"
        ]]

        file_path = "final_attendance.xlsx"
        final_data.to_excel(file_path, index=False)

        return send_file(file_path, as_attachment=True)

    return "File not found!"


# ---------------- VIEW STUDENTS ----------------
@app.route("/students")
def students():
    return send_file("students.csv", as_attachment=False)


# ---------------- ATTENDANCE PAGE ----------------
@app.route("/attendance")
def attendance():

    attendance = pd.read_csv("attendance.csv") if os.path.exists("attendance.csv") else pd.DataFrame()
    students = pd.read_csv("students.csv") if os.path.exists("students.csv") else pd.DataFrame()

    if not attendance.empty and not students.empty:
        data = pd.merge(attendance, students, on="Name", how="left")

        # Fix columns
        if "RegisterNo_y" in data.columns:
            data["RegisterNo"] = data["RegisterNo_y"]

        if "Department" not in data.columns and "Department_y" in data.columns:
            data["Department"] = data["Department_y"]

    else:
        data = attendance

    return render_template(
        "attendance.html",
        attendance=data.to_dict(orient="records")
    )


# ---------------- REPORT PAGE ----------------
@app.route("/report")
def report():

    attendance = pd.read_csv("attendance.csv") if os.path.exists("attendance.csv") else pd.DataFrame()

    if attendance.empty:
        report = pd.DataFrame()
    else:
        report = attendance.groupby("Name").agg(
            Total=("Status", "count"),
            Present=("Status", lambda x: (x == "Present").sum()),
            Late=("Status", lambda x: (x == "Late").sum())
        ).reset_index()

        report["Percentage"] = ((report["Present"] + report["Late"]) / report["Total"]) * 100

    return render_template(
        "report.html",
        report=report.to_dict(orient="records")
    )


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)