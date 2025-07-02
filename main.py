import os
import time
import mysql.connector
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import pandas as pd
from colorama import Fore, init
from typing import List, Tuple

init(autoreset=True)


# ---------------------------- Utilities ---------------------------- #

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input(Fore.YELLOW + "\n(Press Enter to continue...)")


def loading(msg: str, delay: float = 0.4):
    print(Fore.YELLOW + msg, end='', flush=True)
    for _ in range(3):
        time.sleep(delay)
        print('.', end='', flush=True)
    print()


def header(title: str):
    clear_screen()
    print(Fore.MAGENTA + "=" * 60)
    print(Fore.CYAN + f"{title.center(60)}")
    print(Fore.MAGENTA + "=" * 60)


# ------------------------ Database Management ---------------------- #

class DatabaseManager:
    def __init__(self, host='localhost', user='root', password='', database='student_marks'):
        self.conn = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                class VARCHAR(50),
                roll_no VARCHAR(50),
                percentage FLOAT,
                grade VARCHAR(10)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS marks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT,
                subject VARCHAR(255),
                marks FLOAT,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    def insert_student(self, name, student_class, roll_no, percentage, grade) -> int:
        self.cursor.execute("""
            INSERT INTO students (name, class, roll_no, percentage, grade)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, student_class, roll_no, percentage, grade))
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_marks(self, student_id, subjects: List[str], marks: List[float]):
        for subject, mark in zip(subjects, marks):
            self.cursor.execute("""
                INSERT INTO marks (student_id, subject, marks)
                VALUES (%s, %s, %s)
            """, (student_id, subject, mark))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


# ------------------------- Student Data Model ---------------------- #

class Student:
    def __init__(self, name: str, student_class: str, roll_no: str):
        self.name = name
        self.student_class = student_class
        self.roll_no = roll_no
        self.subjects: List[str] = []
        self.marks: List[float] = []
        self.percentage: float = 0.0
        self.grade: str = ""

    def add_subject(self, subject: str, mark: float):
        self.subjects.append(subject.title())
        self.marks.append(mark)

    def calculate_results(self):
        if not self.marks:
            self.percentage = 0.0
            self.grade = "N/A"
            return
        self.percentage = round(sum(self.marks) / (len(self.marks) * 100) * 100, 2)
        self.grade = self.assign_grade()

    def assign_grade(self) -> str:
        p = self.percentage
        return (
            "A+ 🌟" if p >= 90 else
            "A 👍" if p >= 80 else
            "B 🙂" if p >= 70 else
            "C 😐" if p >= 60 else
            "D 😬" if p >= 50 else
            "F 💀"
        )

    def display_report(self):
        header(f"📄 Report for {self.name}")
        print(f"{Fore.CYAN}Name      : {self.name}")
        print(f"Class     : {self.student_class}")
        print(f"Roll No   : {self.roll_no}\n")
        print(Fore.YELLOW + f"{'Subject':<20}{'Marks':>15}")
        print(Fore.MAGENTA + "-" * 35)
        for sub, mark in zip(self.subjects, self.marks):
            print(f"{sub:<20}{mark:>15.2f}")
        print(Fore.MAGENTA + "-" * 35)
        print(f"{'Percentage':<20}{self.percentage:>15.2f}%")
        print(f"{'Grade':<20}{self.grade}\n")
        pause()

    def save_text_report(self):
        filename = f"{self.name.replace(' ', '_')}_Report.txt"
        with open(filename, 'w') as f:
            f.write(f"Student Report - {self.name}\n")
            f.write("=" * 50 + "\n")
            f.write(f"Name     : {self.name}\n")
            f.write(f"Class    : {self.student_class}\n")
            f.write(f"Roll No  : {self.roll_no}\n")
            f.write(f"Percentage: {self.percentage}%\n")
            f.write(f"Grade     : {self.grade}\n\n")
            f.write("Subject-wise Marks:\n")
            for sub, mark in zip(self.subjects, self.marks):
                f.write(f"- {sub}: {mark}/100\n")
        print(Fore.GREEN + f"\n✅ Report saved as {filename}")


# ----------------------- Graphing Functions ----------------------- #

class Visualizer:
    @staticmethod
    def pie_chart(student: Student):
        colors = plt.cm.plasma(np.linspace(0, 1, len(student.subjects)))
        plt.figure(figsize=(8, 8))
        plt.pie(student.marks, labels=student.subjects, autopct='%1.1f%%', colors=colors, startangle=140)
        plt.title(f"{student.name} - Marks Breakdown ({student.percentage}%)", fontsize=14)
        plt.savefig(f"{student.name.replace(' ', '_')}_PieChart.png")
        plt.show()

    @staticmethod
    def bar_graph(student: Student):
        colors = plt.cm.viridis(np.linspace(0, 1, len(student.subjects)))
        plt.figure(figsize=(10, 6))
        bars = plt.bar(student.subjects, student.marks, color=colors, edgecolor='black')
        plt.title(f"{student.name} - Marks per Subject", fontsize=14)
        plt.ylabel("Marks (out of 100)")
        plt.ylim(0, 110)
        for bar in bars:
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f"{bar.get_height():.1f}", ha='center')
        plt.savefig(f"{student.name.replace(' ', '_')}_BarGraph.png")
        plt.show()

    @staticmethod
    def interactive_plot(student: Student):
        df = pd.DataFrame({'Subject': student.subjects, 'Marks': student.marks})
        fig = px.bar(df, x='Subject', y='Marks', color='Subject',
                     title=f"{student.name} - Interactive Marks Chart",
                     text='Marks', template='plotly_dark')
        fig.write_html(f"{student.name.replace(' ', '_')}_InteractiveGraph.html")
        fig.show()


# ------------------------ Application Workflow ------------------- #

class StudentMarksApp:
    def __init__(self):
        self.db = DatabaseManager()

    def run(self):
        while True:
            header("👋 Student Marks Management (Pro Edition)")
            print("1️⃣  Enter Student Details & Report")
            print("2️⃣  Exit")
            choice = input(Fore.CYAN + "\nSelect an option (1 or 2): ").strip()

            if choice == '1':
                self.process_student()
            elif choice == '2':
                print(Fore.YELLOW + "\nGoodbye! Your data is safe. 👋")
                self.db.close()
                break
            else:
                print(Fore.RED + "Invalid choice. Please select 1 or 2.")
                pause()

    def process_student(self):
        header("🚀 Let's Gather Student Information")
        name = input("Full Name: ").strip().title()
        student_class = input("Class: ").strip().upper()
        roll_no = input("Roll Number: ").strip()

        student = Student(name, student_class, roll_no)
        header("📚 Subject & Marks Entry (Type 'done' to finish)")

        while True:
            subject = input("Subject Name: ").strip()
            if subject.lower() == 'done':
                break
            try:
                mark = float(input(f"Marks in {subject} (out of 100): "))
                if 0 <= mark <= 100:
                    student.add_subject(subject, mark)
                else:
                    print(Fore.RED + "Marks must be between 0 and 100.")
            except ValueError:
                print(Fore.RED + "Please enter valid numeric marks.")

        if not student.subjects:
            print(Fore.RED + "\n⚠️ No subjects entered. Returning to menu.")
            pause()
            return

        student.calculate_results()
        student.display_report()
        student.save_text_report()

        student_id = self.db.insert_student(
            student.name, student.student_class, student.roll_no,
            student.percentage, student.grade
        )
        self.db.insert_marks(student_id, student.subjects, student.marks)
        print(Fore.GREEN + "✅ Data stored in MySQL successfully.")
        pause()

        header("🎨 Visualizing Results")
        loading("Generating Pie Chart")
        Visualizer.pie_chart(student)
        loading("Generating Bar Graph")
        Visualizer.bar_graph(student)
        loading("Creating Interactive Plot")
        Visualizer.interactive_plot(student)
        print(Fore.GREEN + "\nAll reports and charts generated successfully!")
        pause()


# --------------------------- Program Start ------------------------- #

if __name__ == "__main__":
    app = StudentMarksApp()
    app.run()
