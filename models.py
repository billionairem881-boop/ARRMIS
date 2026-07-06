from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


# ==========================
# USER MODEL
# ==========================

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    full_name = db.Column(db.String(150), nullable=False)

    role = db.Column(
        db.String(20),
        nullable=False,
        default="student"
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    def __repr__(self):
        return f"<User {self.username}>"



# ===============================
# PROGRAMME MODEL
# ===============================

class Programme(db.Model):
    __tablename__ = "programmes"

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    def __repr__(self):
        return f"<Programme {self.name}>"



# ==========================
# DEPARTMENT MODEL
# ==========================

class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    hod = db.Column(
        db.String(150)
    )

    description = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    students = db.relationship(
        "Student",
        backref="department",
        lazy=True
    )

    lecturers = db.relationship(
        "Lecturer",
        backref="department",
        lazy=True
    )

    courses = db.relationship(
        "Course",
        backref="department",
        lazy=True
    )



# ==========================
# LECTURER MODEL
# ==========================

class Lecturer(db.Model):
    __tablename__ = "lecturers"

    id = db.Column(db.Integer, primary_key=True)

    staff_no = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    full_name = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(30)
    )

    qualification = db.Column(
        db.String(150)
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id")
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    courses = db.relationship(
        "Course",
        backref="lecturer",
        lazy=True
    )



# ==========================
# STUDENT MODEL
# ==========================

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    reg_no = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    full_name = db.Column(
        db.String(150),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    gender = db.Column(
        db.String(20)
    )

    phone = db.Column(
        db.String(30)
    )

    date_of_birth = db.Column(
        db.Date
    )

    address = db.Column(
        db.Text
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id")
    )

    year_of_study = db.Column(
        db.Integer,
        default=1
    )

    semester = db.Column(
        db.String(20)
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



# ==========================
# COURSE MODEL
# ==========================

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    credit_hours = db.Column(
        db.Integer,
        default=3
    )

    semester = db.Column(
        db.String(20)
    )

    level = db.Column(
        db.String(20)
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id")
    )

    lecturer_id = db.Column(
        db.Integer,
        db.ForeignKey("lecturers.id")
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Course {self.code}>"
        # ==========================
# COURSE REGISTRATION MODEL
# ==========================

class CourseRegistration(db.Model):
    __tablename__ = "course_registrations"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    academic_year = db.Column(
        db.String(20),
        nullable=False
    )

    semester = db.Column(
        db.String(20),
        nullable=False
    )

    registration_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        "Student",
        backref=db.backref(
            "registrations",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    course = db.relationship(
        "Course",
        backref=db.backref(
            "registrations",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )


# ==========================
# ATTENDANCE MODEL
# ==========================

class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    date = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Present"
    )

    student = db.relationship(
        "Student",
        backref="attendance_records"
    )

    course = db.relationship(
        "Course",
        backref="attendance_records"
    )


# ==========================
# RESULT MODEL
# ==========================

class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    assignment = db.Column(
        db.Float,
        default=0
    )

    quiz = db.Column(
        db.Float,
        default=0
    )

    exam = db.Column(
        db.Float,
        default=0
    )

    total = db.Column(
        db.Float,
        default=0
    )

    grade = db.Column(
        db.String(5)
    )

    gpa = db.Column(
        db.Float,
        default=0
    )

    semester = db.Column(
        db.String(20)
    )

    academic_year = db.Column(
        db.String(20)
    )

    student = db.relationship(
        "Student",
        backref="results"
    )

    course = db.relationship(
        "Course",
        backref="results"
    )


# ==========================
# TRANSCRIPT MODEL
# ==========================

class Transcript(db.Model):
    __tablename__ = "transcripts"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    cgpa = db.Column(
        db.Float,
        default=0
    )

    total_credits = db.Column(
        db.Integer,
        default=0
    )

    classification = db.Column(
        db.String(50)
    )

    generated_on = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        "Student",
        backref="transcript",
        uselist=False
    )


# ==========================
# ANNOUNCEMENT MODEL
# ==========================

class Announcement(db.Model):
    __tablename__ = "announcements"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    posted_by = db.Column(
        db.String(100)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ==========================
# NOTIFICATION MODEL
# ==========================

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    recipient = db.Column(
        db.String(50),
        default="all"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ==========================
# ACADEMIC CALENDAR MODEL
# ==========================

class AcademicCalendar(db.Model):
    __tablename__ = "academic_calendar"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    category = db.Column(
        db.String(50)
    )

    description = db.Column(
        db.Text
    )

    start_date = db.Column(
        db.Date,
        nullable=False
    )

    end_date = db.Column(
        db.Date,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    # ==========================
# LEARNING MATERIAL MODEL
# ==========================

class LearningMaterial(db.Model):
    __tablename__ = "learning_materials"

    id = db.Column(db.Integer, primary_key=True)

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    lecturer_id = db.Column(
        db.Integer,
        db.ForeignKey("lecturers.id"),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    file_name = db.Column(
        db.String(255)
    )

    file_path = db.Column(
        db.String(255)
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    course = db.relationship(
        "Course",
        backref="learning_materials"
    )

    lecturer = db.relationship(
        "Lecturer",
        backref="learning_materials"
    )


# ==========================
# ASSIGNMENT MODEL
# ==========================

class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    instructions = db.Column(
        db.Text
    )

    due_date = db.Column(
        db.Date
    )

    max_marks = db.Column(
        db.Integer,
        default=100
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    course = db.relationship(
        "Course",
        backref="assignments"
    )


# ==========================
# ASSIGNMENT SUBMISSION MODEL
# ==========================

class AssignmentSubmission(db.Model):
    __tablename__ = "assignment_submissions"

    id = db.Column(db.Integer, primary_key=True)

    assignment_id = db.Column(
        db.Integer,
        db.ForeignKey("assignments.id"),
        nullable=False
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    file_path = db.Column(
        db.String(255)
    )

    submitted_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    score = db.Column(
        db.Float,
        default=0
    )

    feedback = db.Column(
        db.Text
    )

    graded = db.Column(
        db.Boolean,
        default=False
    )

    assignment = db.relationship(
        "Assignment",
        backref="submissions"
    )

    student = db.relationship(
        "Student",
        backref="assignment_submissions"
    )


# ==========================
# QUIZ MODEL
# ==========================

class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    instructions = db.Column(
        db.Text
    )

    duration = db.Column(
        db.Integer,
        default=30
    )

    total_marks = db.Column(
        db.Integer,
        default=100
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    course = db.relationship(
        "Course",
        backref="quizzes")


# ==========================
# QUIZ QUESTION MODEL
# ==========================

class QuizQuestion(db.Model):
    __tablename__ = "quiz_questions"

    id = db.Column(db.Integer, primary_key=True)

    quiz_id = db.Column(
        db.Integer,
        db.ForeignKey("quizzes.id"),
        nullable=False
    )

    question = db.Column(
        db.Text,
        nullable=False
    )

    option_a = db.Column(db.String(255))
    option_b = db.Column(db.String(255))
    option_c = db.Column(db.String(255))
    option_d = db.Column(db.String(255))

    correct_answer = db.Column(
        db.String(1),
        nullable=False
    )

    marks = db.Column(
        db.Integer,
        default=1
    )

    quiz = db.relationship(
        "Quiz",
        backref="questions"
    )


# ==========================
# EXAM MODEL
# ==========================

class Exam(db.Model):
    __tablename__ = "exams"

    id = db.Column(db.Integer, primary_key=True)

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    instructions = db.Column(
        db.Text
    )

    duration = db.Column(
        db.Integer,
        default=120
    )

    total_marks = db.Column(
        db.Integer,
        default=100
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    course = db.relationship(
        "Course",
        backref="exams"
    )


# ==========================
# EXAM QUESTION MODEL
# ==========================

class ExamQuestion(db.Model):
    __tablename__ = "exam_questions"

    id = db.Column(db.Integer, primary_key=True)

    exam_id = db.Column(
        db.Integer,
        db.ForeignKey("exams.id"),
        nullable=False
    )

    question = db.Column(
        db.Text,
        nullable=False
    )

    option_a = db.Column(db.String(255))
    option_b = db.Column(db.String(255))
    option_c = db.Column(db.String(255))
    option_d = db.Column(db.String(255))

    correct_answer = db.Column(
        db.String(1),
        nullable=False
    )

    marks = db.Column(
        db.Integer,
        default=1
    )

    exam = db.relationship(
        "Exam",
        backref="questions"
    )
    # ==========================
# DISCUSSION FORUM MODEL
# ==========================

class DiscussionPost(db.Model):
    __tablename__ = "discussion_posts"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    content = db.Column(db.Text, nullable=False)

    author = db.Column(db.String(150), nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    replies = db.relationship(
        "DiscussionReply",
        backref="post",
        lazy=True,
        cascade="all, delete-orphan"
    )


# ==========================
# DISCUSSION REPLY MODEL
# ==========================

class DiscussionReply(db.Model):
    __tablename__ = "discussion_replies"

    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("discussion_posts.id"),
        nullable=False
    )

    author = db.Column(
        db.String(150),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ==========================
# PAYMENT MODEL
# ==========================

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    semester = db.Column(
        db.String(30),
        nullable=False
    )

    payment_method = db.Column(
        db.String(50)
    )

    reference = db.Column(
        db.String(150),
        unique=True
    )

    status = db.Column(
        db.String(30),
        default="Paid"
    )

    payment_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        "Student",
        backref="payments"
    )


# ==========================
# LIBRARY BOOK MODEL
# ==========================

class LibraryBook(db.Model):
    __tablename__ = "library_books"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    author = db.Column(
        db.String(150),
        nullable=False
    )

    category = db.Column(
        db.String(100)
    )

    isbn = db.Column(
        db.String(50),
        unique=True
    )

    copies = db.Column(
        db.Integer,
        default=1
    )

    available = db.Column(
        db.Boolean,
        default=True
    )

    description = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ==========================
# AUDIT LOG MODEL
# ==========================

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        nullable=False
    )

    action = db.Column(
        db.String(255),
        nullable=False
    )

    ip_address = db.Column(
        db.String(50)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ==========================
# SYSTEM SETTINGS MODEL
# ==========================

class SystemSetting(db.Model):
    __tablename__ = "system_settings"

    id = db.Column(db.Integer, primary_key=True)

    institution_name = db.Column(
        db.String(255),
        default="University"
    )

    institution_email = db.Column(
        db.String(150)
    )

    institution_phone = db.Column(
        db.String(50)
    )

    institution_address = db.Column(
        db.Text
    )

    academic_year = db.Column(
        db.String(20)
    )

    current_semester = db.Column(
        db.String(20)
    )

    logo = db.Column(
        db.String(255)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )