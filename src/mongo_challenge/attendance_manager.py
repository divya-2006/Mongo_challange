from pymongo import MongoClient
from pymongo.errors import PyMongoError

MONGO_URL = "url"

class AttendanceManager:
    def __init__(self, connection_string, database_name):
        mongo_client = MongoClient(connection_string)
        database = mongo_client[database_name]
        self.students = database["students"]
        self.attendance = database["attendance"]
        self.students.create_index("USN", unique=True)
        self.attendance.create_index([("USN", 1), ("date", 1)])

    def add_student(self, name, USN, email, course):
        try:
            student = self.students.find_one({"USN": USN})
            if student:
                print("This roll number already exists")
                return
            student_data = {
                "name": name,
                "USN": USN,
                "email": email,
                "course": course
            }
            self.students.insert_one(student_data)
            print("Student added")
        except PyMongoError:
            print("Database error")

    def add_attendance(self, USN, date, status):
        if status not in ["Present", "Absent"]:
            print("Invalid attendance status")
            return
        try:
            student = self.students.find_one({"USN": USN})
            if not student:
                print("Student does not exist")
                return
            attendance_data = {
                "USN": USN,
                "date": date,
                "status": status
            }
            self.attendance.insert_one(attendance_data)
            print("Attendance added")
        except PyMongoError:
            print("Database error")

    def get_all_attendance(self):
        try:
            attendance_records = self.attendance.find()
            student_list = []
            for record in attendance_records:
                student_list.append(record)
            return student_list
        except PyMongoError:
            print("Database error")
            return []

    def delete_student(self, USN):
        try:
            student = self.students.find_one({"USN": USN})
            if not student:
                print("Student does not exist")
                return
            self.students.delete_one({"USN": USN})
            print("Student deleted")
        except PyMongoError:
            print("Database error")

    def find_student(self, USN):
        try:
            student = self.students.find_one({"USN": USN})
            if not student:
                print("Student does not exist")
                return
            return student
        except PyMongoError:
            print("Database error")

    def get_student_attendance(self, USN):
        try:
            student = self.students.find_one({"USN": USN})
            if not student:
                print("Student does not exist")
                return []
            attendance_records = self.attendance.find({"USN": USN})
            student_list = []
            for record in attendance_records:
                student_list.append(record)
            return student_list
        except PyMongoError:
            print("Database error")
            return []

    def attendance_percentage(self, USN):
        try:
            student = self.students.find_one({"USN": USN})
            if not student:
                print("Student does not exist")
                return
            student_list = list(self.attendance.find({"USN": USN}))
            if len(student_list) == 0:
                print("No attendance found")
                return
            present = 0
            for i in student_list:
                if i["status"] == "Present":
                    present = present + 1
            total = len(student_list)
            percentage = (present / total) * 100
            print("Attendance percentage:", round(percentage, 2))
        except PyMongoError:
            print("Database error")

attend_manager = AttendanceManager(MONGO_URL, "college_attendance")
attend_manager.add_student("Divya", "1", "divya@gmail.com", "Mechanical")
attend_manager.add_attendance("1", "2026-09-19", "Present")
print(attend_manager.get_all_attendance())
print(attend_manager.find_student("1"))
print(attend_manager.get_student_attendance("1"))