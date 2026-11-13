"""
What is the most complicated code you have written independently without AI
or anyone else's assistance?

Ans- A Smart Student Performance Analysis System I developed using Python.
It takes student details and marks in multiple subjects, calculates total marks, 
averages, percentages and grades, and ranks students based on their performance. 
It also identifies students who are at risk of failing, performs subject-wise analysis, 
calculates class statistics, and generates performance reports. I used OOP concepts, classes,
dictionaries, lists, sorting, exception handling and CSV file handling to build it. 
The most challenging part was connecting all the calculations and analysis features while ensuring the student records were saved and loaded correctly.
"""


import csv
import os
from statistics import mean, median, stdev
from datetime import datetime


class Student:
    def __init__(self, roll_no, name, marks):
        self.roll_no = roll_no
        self.name = name
        self.marks = marks

    def get_total(self):
        return sum(self.marks.values())

    def get_average(self):
        return mean(self.marks.values())

    def get_percentage(self):
        return self.get_total() / len(self.marks)

    def get_grade(self):
        percentage = self.get_percentage()

        if percentage >= 90:
            return "A+"
        elif percentage >= 80:
            return "A"
        elif percentage >= 70:
            return "B"
        elif percentage >= 60:
            return "C"
        elif percentage >= 40:
            return "D"
        return "F"

    def get_status(self):
        if min(self.marks.values()) < 35:
            return "AT RISK"
        return "PASS"


class PerformanceAnalyzer:

    def __init__(self):
        self.students = []
        self.subjects = [
            "Python", "Mathematics",
            "Database", "Machine Learning"
        ]
        self.filename = "student_records.csv"

    def add_student(self):
        try:
            roll = int(input("\nEnter Roll Number: "))

            if any(s.roll_no == roll for s in self.students):
                print("Roll number already exists.")
                return

            name = input("Enter Student Name: ").strip()

            if not name:
                print("Name cannot be empty.")
                return

            marks = {}

            for subject in self.subjects:
                while True:
                    try:
                        score = float(
                            input(f"Enter marks in {subject}: ")
                        )

                        if 0 <= score <= 100:
                            marks[subject] = score
                            break

                        print("Marks must be between 0 and 100.")

                    except ValueError:
                        print("Please enter a valid number.")

            student = Student(roll, name, marks)
            self.students.append(student)

            print("\nStudent added successfully!")

        except ValueError:
            print("Invalid roll number.")

    def display_students(self):
        if not self.students:
            print("\nNo student records available.")
            return

        print("\n" + "=" * 85)
        print(f"{'ROLL':<10}{'NAME':<20}{'TOTAL':<10}"
              f"{'AVERAGE':<12}{'GRADE':<10}{'STATUS':<12}")
        print("=" * 85)

        for student in self.students:
            print(
                f"{student.roll_no:<10}"
                f"{student.name:<20}"
                f"{student.get_total():<10.1f}"
                f"{student.get_average():<12.2f}"
                f"{student.get_grade():<10}"
                f"{student.get_status():<12}"
            )

    def calculate_rankings(self):
        ranked = sorted(
            self.students,
            key=lambda s: (
                s.get_average(),
                s.get_total()
            ),
            reverse=True
        )

        print("\nSTUDENT RANKINGS")
        print("-" * 50)

        for position, student in enumerate(ranked, 1):
            print(
                f"Rank {position}: {student.name} "
                f"({student.get_average():.2f}%)"
            )

    def subject_analysis(self):
        if not self.students:
            print("No data available.")
            return

        print("\nSUBJECT-WISE ANALYSIS")
        print("-" * 55)

        for subject in self.subjects:
            scores = [
                student.marks[subject]
                for student in self.students
            ]

            print(f"\nSubject: {subject}")
            print(f"Average: {mean(scores):.2f}")
            print(f"Highest: {max(scores):.2f}")
            print(f"Lowest: {min(scores):.2f}")

            if len(scores) > 1:
                print(f"Standard Deviation: {stdev(scores):.2f}")
            else:
                print("Standard Deviation: N/A")

    def identify_weak_students(self):
        print("\nSTUDENTS REQUIRING ATTENTION")
        print("-" * 50)

        flagged = [
            s for s in self.students
            if s.get_status() == "AT RISK"
            or s.get_average() < 50
        ]

        if not flagged:
            print("No students currently flagged.")
            return

        for student in flagged:
            weak_subjects = [
                subject for subject, score in student.marks.items()
                if score < 50
            ]

            print(f"\nName: {student.name}")
            print(f"Average: {student.get_average():.2f}")
            print(f"Weak Subjects: {', '.join(weak_subjects)}")

    def class_statistics(self):
        if not self.students:
            print("No records available.")
            return

        averages = [
            student.get_average()
            for student in self.students
        ]

        print("\nCLASS PERFORMANCE STATISTICS")
        print("-" * 50)
        print(f"Total Students: {len(self.students)}")
        print(f"Class Average: {mean(averages):.2f}")
        print(f"Median Score: {median(averages):.2f}")
        print(f"Highest Average: {max(averages):.2f}")
        print(f"Lowest Average: {min(averages):.2f}")

        passed = sum(
            1 for s in self.students
            if s.get_status() == "PASS"
        )

        pass_percentage = (passed / len(self.students)) * 100

        print(f"Pass Percentage: {pass_percentage:.2f}%")

    def save_records(self):
        try:
            with open(
                self.filename, "w", newline="", encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                headers = ["Roll Number", "Name"] + self.subjects
                headers += ["Total", "Average", "Grade", "Status"]

                writer.writerow(headers)

                for student in self.students:
                    row = [
                        student.roll_no,
                        student.name
                    ]

                    row.extend(
                        student.marks[sub]
                        for sub in self.subjects
                    )

                    row.extend([
                        student.get_total(),
                        student.get_average(),
                        student.get_grade(),
                        student.get_status()
                    ])

                    writer.writerow(row)

            print("\nRecords saved successfully!")

        except OSError as error:
            print(f"File error: {error}")

    def load_records(self):
        if not os.path.exists(self.filename):
            print("No previously saved records found.")
            return

        try:
            with open(
                self.filename, "r", newline="", encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)
                loaded = []

                for row in reader:
                    marks = {
                        subject: float(row[subject])
                        for subject in self.subjects
                    }

                    student = Student(
                        int(row["Roll Number"]),
                        row["Name"],
                        marks
                    )

                    loaded.append(student)

                self.students = loaded

            print(f"\nLoaded {len(self.students)} student records.")

        except (OSError, ValueError, KeyError) as error:
            print(f"Unable to load records: {error}")

    def generate_report(self):
        if not self.students:
            print("No data available for report generation.")
            return

        filename = "performance_report.txt"

        try:
            with open(filename, "w", encoding="utf-8") as file:

                file.write("STUDENT PERFORMANCE REPORT\n")
                file.write("=" * 45 + "\n")
                file.write(
                    f"Generated: {datetime.now()}\n\n"
                )

                file.write(
                    f"Total Students: {len(self.students)}\n"
                )

                file.write(
                    f"Class Average: "
                    f"{mean(s.get_average() for s in self.students):.2f}\n\n"
                )

                ranked = sorted(
                    self.students,
                    key=lambda s: s.get_average(),
                    reverse=True
                )

                file.write("TOP PERFORMERS\n")

                for student in ranked[:3]:
                    file.write(
                        f"{student.name} - "
                        f"{student.get_average():.2f}%\n"
                    )

                file.write("\nSTUDENT DETAILS\n")

                for student in self.students:
                    file.write(
                        f"\n{student.name} | "
                        f"Grade: {student.get_grade()} | "
                        f"Status: {student.get_status()}\n"
                    )

            print(f"\nReport generated: {filename}")

        except OSError as error:
            print(f"Report generation failed: {error}")

    def run(self):
        self.load_records()

        while True:
            print("\n" + "=" * 50)
            print(" SMART STUDENT PERFORMANCE ANALYSIS SYSTEM")
            print("=" * 50)

            print("1. Add Student")
            print("2. Display Student Records")
            print("3. Calculate Student Rankings")
            print("4. Subject-wise Analysis")
            print("5. Identify Weak Students")
            print("6. Class Statistics")
            print("7. Save Records")
            print("8. Generate Performance Report")
            print("9. Exit")

            choice = input("\nEnter your choice: ").strip()

            operations = {
                "1": self.add_student,
                "2": self.display_students,
                "3": self.calculate_rankings,
                "4": self.subject_analysis,
                "5": self.identify_weak_students,
                "6": self.class_statistics,
                "7": self.save_records,
                "8": self.generate_report
            }

            if choice == "9":
                self.save_records()
                print("Exiting system. Goodbye!")
                break

            operation = operations.get(choice)

            if operation:
                operation()
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    system = PerformanceAnalyzer()
    system.run()
