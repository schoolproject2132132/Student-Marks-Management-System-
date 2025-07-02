# Student-Marks-Management-System-
Student Marks Management System - Pro Edition

Overview

The Student Marks Management System - Pro Edition is a next-generation, production-grade Python application that allows you to manage student academic records, visualize their marks, and store everything securely in a MySQL database. It features a modern, modular design with Object-Oriented Programming (OOP), advanced data visualization, and a user-friendly, interactive command-line interface.

This project surpasses basic AI-generated templates by providing:

Deep modular structure

Full MySQL integration

Data validation & error handling

High-quality Matplotlib and Plotly visual reports

Text-based reports saved locally

Future-proof, clean codebase ready for expansion

Features

✅ Fully Object-Oriented design for scalability✅ Modern, human-friendly CLI experience with color outputs✅ Student details and marks stored in MySQL (localhost)✅ Auto creation of required database tables✅ Subject-wise marks entry with percentage and grade calculation✅ Generates:

Text-based student report file

Pie Chart of marks distribution (PNG)

Bar Graph of marks per subject (PNG)

Interactive Plotly chart (HTML)
✅ Secure parameterized SQL queries✅ Cross-platform support (Windows/Linux/Mac)✅ Modular, maintainable code exceeding 250+ lines✅ Extensible architecture for future features

Prerequisites

Make sure you have the following installed:

Python Libraries:

pip install matplotlib plotly pandas numpy mysql-connector-python colorama

MySQL Server:

Ensure MySQL is installed and running on localhost (port 3306).

MySQL Setup:

CREATE DATABASE student_marks;

Update the database connection credentials in DatabaseManager class if you have a different user or password:

self.conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',  # Update this if you set a password
    database='student_marks'
)

Project Structure

student_marks_system.py      # Main Python application
README.md                    # This project report and instructions
*_Report.txt                 # Generated student text reports
*_PieChart.png               # Pie chart image of marks distribution
*_BarGraph.png               # Bar graph image of subject marks
*_InteractiveGraph.html      # Interactive Plotly chart file

How to Run the Application

Make sure your MySQL server is running.

Run the main program:

python student_marks_system.py

Follow the friendly prompts to:

Enter student details

Enter subject names and marks

View calculated percentage and grade

Generate and view graphical reports

All data is stored securely in your MySQL database.

Text reports and visual charts are saved locally.

Technical Details

Uses Matplotlib for static Pie and Bar charts

Uses Plotly for interactive HTML graphs

Secure SQL inserts prevent injection attacks

Supports unlimited subjects per student

Designed with separation of concerns:

DatabaseManager handles all database operations

Student class manages student data and calculations

Visualizer class handles charts and reporting

StudentMarksApp orchestrates the workflow

Follows clean coding standards with type hints and docstrings

Future Improvements (Planned)

Export reports to PDF/Excel

Multi-student batch processing

Login system with user roles (Admin/Student)

Search, edit, and delete student records

Performance analytics across terms

More advanced error handling & unit tests

Support

If you encounter issues or want more advanced features, feel free to extend the code or request enhancements.

Final Notes

This project exceeds typical boilerplate code with a deep, structured, professional-grade design—ready for academic institutions, student portals, or as a learning resource for advanced Python, MySQL, and data visualization integration.

Built with ❤️ for developers seeking quality beyond AI generators.

