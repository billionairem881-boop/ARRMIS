from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    SelectField,
    IntegerField,
    FloatField,
    TextAreaField,
    DateField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange
)


# =====================================
# LOGIN FORM
# =====================================

class LoginForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")


# =====================================
# STUDENT FORM
# =====================================

class StudentForm(FlaskForm):

    reg_no = StringField(
        "Registration Number",
        validators=[DataRequired()]
    )

    full_name = StringField(
        "Full Name",
        validators=[DataRequired()]
    )

    email = StringField(
        "Email",
        validators=[Email()]
    )

    gender = SelectField(
        "Gender",
        choices=[
            ("Male", "Male"),
            ("Female", "Female")
        ]
    )

    phone = StringField("Phone")

    department = SelectField(
        "Department",
        coerce=int
    )

    year = IntegerField("Year")

    semester = StringField("Semester")

    submit = SubmitField("Save Student")


# =====================================
# LECTURER FORM
# =====================================

class LecturerForm(FlaskForm):

    staff_no = StringField(
        "Staff Number",
        validators=[DataRequired()]
    )

    full_name = StringField(
        "Full Name",
        validators=[DataRequired()]
    )

    email = StringField(
        "Email",
        validators=[Email()]
    )

    phone = StringField("Phone")

    qualification = StringField("Qualification")

    submit = SubmitField("Save Lecturer")


# =====================================
# DEPARTMENT FORM
# =====================================

class DepartmentForm(FlaskForm):

    code = StringField(
        "Department Code",
        validators=[DataRequired()]
    )

    name = StringField(
        "Department Name",
        validators=[DataRequired()]
    )

    hod = StringField("Head of Department")

    description = TextAreaField("Description")

    submit = SubmitField("Save Department")


# =====================================
# COURSE FORM
# =====================================

class CourseForm(FlaskForm):

    code = StringField(
        "Course Code",
        validators=[DataRequired()]
    )

    title = StringField(
        "Course Title",
        validators=[DataRequired()]
    )

    credit_hours = IntegerField(
        "Credit Hours",
        validators=[NumberRange(min=1)]
    )

    semester = StringField("Semester")

    submit = SubmitField("Save Course")


# =====================================
# ASSIGNMENT FORM
# =====================================

class AssignmentForm(FlaskForm):

    title = StringField(
        "Assignment Title",
        validators=[DataRequired()]
    )

    instructions = TextAreaField("Instructions")

    due_date = DateField(
        "Due Date"
    )

    submit = SubmitField("Save Assignment")


# =====================================
# QUIZ FORM
# =====================================

class QuizForm(FlaskForm):

    title = StringField(
        "Quiz Title",
        validators=[DataRequired()]
    )

    duration = IntegerField("Duration")

    total_marks = IntegerField("Total Marks")

    submit = SubmitField("Save Quiz")


# =====================================
# EXAM FORM
# =====================================

class ExamForm(FlaskForm):

    title = StringField(
        "Exam Title",
        validators=[DataRequired()]
    )

    duration = IntegerField("Duration")

    total_marks = IntegerField("Total Marks")

    submit = SubmitField("Save Exam")


# =====================================
# PAYMENT FORM
# =====================================

class PaymentForm(FlaskForm):

    amount = FloatField(
        "Amount",
        validators=[DataRequired()]
    )

    payment_method = StringField(
        "Payment Method"
    )

    reference = StringField(
        "Reference Number"
    )

    submit = SubmitField("Record Payment")


# =====================================
# LIBRARY FORM
# =====================================

class LibraryBookForm(FlaskForm):

    title = StringField(
        "Book Title",
        validators=[DataRequired()]
    )

    author = StringField(
        "Author",
        validators=[DataRequired()]
    )

    category = StringField("Category")

    isbn = StringField("ISBN")

    submit = SubmitField("Save Book")