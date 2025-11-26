from datetime import datetime

class Student:
    all_students = []

    def __init__(self, name):
        self.name = name
        self._enrollments = []  # all enrollments for this student
        self._grades = {}       # enrollment -> grade
        Student.all_students.append(self)

    def enroll(self, enrollment):
        if not isinstance(enrollment, Enrollment):
            raise Exception("Must be an Enrollment instance")
        self._enrollments.append(enrollment)

    def course_count(self):
        """Aggregate method: number of courses student is enrolled in"""
        return len(self._enrollments)

    def aggregate_average_grade(self):
        """Aggregate method: average grade across all courses"""
        if not self._grades:
            return 0
        total_grades = sum(self._grades.values())
        num_courses = len(self._grades)
        return total_grades / num_courses


class Course:
    all_courses = []

    def __init__(self, name):
        self.name = name
        self._enrollments = []  # all enrollments for this course
        Course.all_courses.append(self)

    def add_enrollment(self, enrollment):
        if not isinstance(enrollment, Enrollment):
            raise Exception("Must be an Enrollment instance")
        self._enrollments.append(enrollment)

    def student_count(self):
        """Aggregate method: number of students in this course"""
        return len(self._enrollments)


class Enrollment:
    all = []

    def __init__(self, student, course, enrollment_date=None, grade=None):
        if not isinstance(student, Student) or not isinstance(course, Course):
            raise Exception("student must be Student and course must be Course instances")
        self.student = student
        self.course = course
        self.enrollment_date = enrollment_date or datetime.now()
        self.grade = grade

        # Link enrollment to student and course
        student.enroll(self)
        course.add_enrollment(self)
        if grade is not None:
            student._grades[self] = grade

        Enrollment.all.append(self)

    def get_enrollment_date(self):
        return self.enrollment_date

    @classmethod
    def aggregate_enrollments_per_day(cls):
        """Aggregate method: count enrollments by day"""
        enrollment_count = {}
        for enrollment in cls.all:
            date = enrollment.get_enrollment_date().date()
            enrollment_count[date] = enrollment_count.get(date, 0) + 1
        return enrollment_count


# --- Example usage ---

# Create students
alice = Student("Alice")
bob = Student("Bob")

# Create courses
math = Course("Math")
history = Course("History")

# Enroll students
Enrollment(alice, math, grade=90)
Enrollment(alice, history, grade=85)
Enrollment(bob, math, grade=75)

# Test aggregate methods
print(alice.course_count())                 # 2
print(alice.aggregate_average_grade())     # 87.5
print(math.student_count())                # 2
print(Enrollment.aggregate_enrollments_per_day())  # {today's date: 3}
