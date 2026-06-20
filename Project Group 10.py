import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import os

# ==========================
# FILE SETUP
# ==========================

USERS_FILE = "users.csv"
RECORDS_FILE = "student_records.csv"

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password"])
        writer.writerow(["admin", "admin123"])

if not os.path.exists(RECORDS_FILE):
    with open(RECORDS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "StudentID", "StudentName", "Level",
            "Score1", "Score2", "Score3", "Score4",
            "Total", "Average", "Grade", "Comment"
        ])

# ==========================
# LOGIN FUNCTION
# ==========================

def login():

    username = username_entry.get()
    password = password_entry.get()

    with open(USERS_FILE, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row["username"] == username and row["password"] == password:
                login_window.destroy()
                open_main_system(username)
                return

    messagebox.showerror("Login Failed", "Invalid Username or Password")


# ==========================
# MAIN SYSTEM
# ==========================

def open_main_system(current_user):

    root = tk.Tk()
    root.title("Student Academic Portal System")
    root.geometry("950x700")

    records = []

    # -----------------------
    # FUNCTIONS
    # -----------------------

    def calculate():

        try:

            s1 = float(score1_entry.get())
            s2 = float(score2_entry.get())
            s3 = float(score3_entry.get())
            s4 = float(score4_entry.get())

            total = s1 + s2 + s3 + s4
            average = total / 4

            if average >= 70:
                grade = "A"
                comment = "Excellent"

            elif average >= 60:
                grade = "B"
                comment = "Very Good"

            elif average >= 50:
                grade = "C"
                comment = "Good"

            elif average >= 40:
                grade = "D"
                comment = "Fair"

            else:
                grade = "F"
                comment = "Fail"

            return total, average, grade, comment

        except:
            messagebox.showerror(
                "Error",
                "Please enter valid scores."
            )
            return None

    def save_record():

        result = calculate()

        if result is None:
            return

        total, average, grade, comment = result

        row = [
            student_id_entry.get(),
            student_name_entry.get(),
            level_combo.get(),
            score1_entry.get(),
            score2_entry.get(),
            score3_entry.get(),
            score4_entry.get(),
            total,
            round(average, 2),
            grade,
            comment
        ]

        with open(RECORDS_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        output.delete(1.0, tk.END)

        output.insert(
            tk.END,
            "Record Saved Successfully\n\n"
            f"Grade: {grade}\n"
            f"Comment: {comment}"
        )

        messagebox.showinfo(
            "Saved",
            "Record saved successfully."
        )

    def display_records():

        output.delete(1.0, tk.END)

        with open(RECORDS_FILE, "r") as f:

            reader = csv.reader(f)

            for row in reader:
                output.insert(
                    tk.END,
                    " | ".join(row) + "\n"
                )

    def search_record():

        keyword = simpledialog.askstring(
            "Search",
            "Enter Student ID or Name"
        )

        if not keyword:
            return

        output.delete(1.0, tk.END)

        found = False

        with open(RECORDS_FILE, "r") as f:

            reader = csv.reader(f)

            for row in reader:

                if keyword.lower() in str(row).lower():
                    output.insert(
                        tk.END,
                        " | ".join(row) + "\n"
                    )
                    found = True

        if not found:
            output.insert(
                tk.END,
                "No record found."
            )

    def add_user():

        new_user = simpledialog.askstring(
            "New User",
            "Enter Username"
        )

        new_pass = simpledialog.askstring(
            "Password",
            "Enter Password"
        )

        if new_user and new_pass:

            with open(USERS_FILE, "a", newline="") as f:

                writer = csv.writer(f)

                writer.writerow(
                    [new_user, new_pass]
                )

            messagebox.showinfo(
                "Success",
                "User added successfully."
            )

    def clear_fields():

        student_id_entry.delete(0, tk.END)
        student_name_entry.delete(0, tk.END)

        score1_entry.delete(0, tk.END)
        score2_entry.delete(0, tk.END)
        score3_entry.delete(0, tk.END)
        score4_entry.delete(0, tk.END)

        level_combo.set("")

        output.delete(1.0, tk.END)

    def exit_system():

        if messagebox.askyesno(
            "Exit",
            "Are you sure?"
        ):
            root.destroy()

    # -----------------------
    # GUI
    # -----------------------

    title = tk.Label(
        root,
        text="STUDENT ACADEMIC PORTAL SYSTEM",
        font=("Arial", 18, "bold")
    )

    title.pack(pady=10)

    tk.Label(
        root,
        text=f"Logged in as: {current_user}"
    ).pack()

    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Label(frame, text="Student ID").grid(row=0, column=0)
    student_id_entry = tk.Entry(frame)
    student_id_entry.grid(row=0, column=1)

    tk.Label(frame, text="Student Name").grid(row=1, column=0)
    student_name_entry = tk.Entry(frame)
    student_name_entry.grid(row=1, column=1)

    tk.Label(frame, text="Level").grid(row=2, column=0)

    level_combo = ttk.Combobox(
        frame,
        values=[
            "Primary School",
            "Junior Secondary School",
            "Senior Secondary School",
            "University"
        ]
    )

    level_combo.grid(row=2, column=1)

    tk.Label(frame, text="Score 1").grid(row=3, column=0)
    score1_entry = tk.Entry(frame)
    score1_entry.grid(row=3, column=1)

    tk.Label(frame, text="Score 2").grid(row=4, column=0)
    score2_entry = tk.Entry(frame)
    score2_entry.grid(row=4, column=1)

    tk.Label(frame, text="Score 3").grid(row=5, column=0)
    score3_entry = tk.Entry(frame)
    score3_entry.grid(row=5, column=1)

    tk.Label(frame, text="Score 4").grid(row=6, column=0)
    score4_entry = tk.Entry(frame)
    score4_entry.grid(row=6, column=1)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Calculate",
        command=lambda: output.insert(
            tk.END,
            str(calculate()) + "\n"
        )
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame,
        text="Save Record",
        command=save_record
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        button_frame,
        text="Search",
        command=search_record
    ).grid(row=0, column=2, padx=5)

    tk.Button(
        button_frame,
        text="Display Records",
        command=display_records
    ).grid(row=0, column=3, padx=5)

    tk.Button(
        button_frame,
        text="Add User",
        command=add_user
    ).grid(row=0, column=4, padx=5)

    tk.Button(
        button_frame,
        text="Clear",
        command=clear_fields
    ).grid(row=0, column=5, padx=5)

    tk.Button(
        button_frame,
        text="Exit",
        command=exit_system
    ).grid(row=0, column=6, padx=5)

    output = tk.Text(
        root,
        width=110,
        height=20
    )

    output.pack(pady=10)

    root.mainloop()


# ==========================
# LOGIN WINDOW
# ==========================

login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("350x250")

tk.Label(
    login_window,
    text="ADMIN LOGIN",
    font=("Arial", 16, "bold")
).pack(pady=15)

tk.Label(login_window, text="Username").pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Password").pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Button(
    login_window,
    text="Login",
    command=login
).pack(pady=15)

login_window.mainloop()

