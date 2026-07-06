from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app import app, db
from forms import LoginForm

from models import (
    User,
    Student,
    Lecturer,
    Department,
    Programme,
    Course,
    CourseRegistration,
    Attendance,
    Result,
    Transcript,
    Announcement,
    Notification,
    AcademicCalendar,
    LearningMaterial,
    Assignment,
    AssignmentSubmission,
    Quiz,
    QuizQuestion,
    Exam,
    ExamQuestion,
    DiscussionPost,
    DiscussionReply,
    Payment,
    LibraryBook,
    AuditLog,
    SystemSetting
)

from functools import wraps
from datetime import datetime
def role_required(*roles):

    def decorator(f):

        @wraps(f)

        def decorated_function(*args, **kwargs):

            if not current_user.is_authenticated:

                return redirect(url_for("login"))

            if current_user.role not in roles:

                flash("Access denied.", "danger")

                return redirect(url_for("dashboard"))

            return f(*args, **kwargs)

        return decorated_function

    return decorator
@app.route("/")
def home():

    if current_user.is_authenticated:

        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))
@app.route("/login", methods=["GET", "POST"])
def login():
    form=LoginForm()

    if form.validate_on_submit():

        username = form.username.data

        password = form.password.data

        user = User.query.filter_by(
            username=username
        ).first()

        if user and user.check_password(password):

            login_user(user)

            flash(
                "Login successful.",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid username or password.",
            "danger"
        )

    return render_template("login.html",form=form)
@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(url_for("login"))
@app.route("/dashboard")
@login_required
def dashboard():

    stats = {

        "students": Student.query.count(),

        "lecturers": Lecturer.query.count(),

        "departments": Department.query.count(),

        "courses": Course.query.count(),

        "registrations": CourseRegistration.query.count(),

        "results": Result.query.count(),

        "assignments": Assignment.query.count(),

        "quizzes": Quiz.query.count(),

        "payments": Payment.query.count(),

        "books": LibraryBook.query.count()

    }

    announcements = Announcement.query.order_by(
        Announcement.created_at.desc()
    ).limit(5).all()

    notifications = Notification.query.order_by(
        Notification.created_at.desc()
    ).limit(5).all()

    calendar = AcademicCalendar.query.order_by(
        AcademicCalendar.start_date
    ).limit(5).all()

    return render_template(
        "dashboard.html",
        stats=stats,
        announcements=announcements,
        notifications=notifications,
        calendar=calendar
    )
# ==========================================
# STUDENT MANAGEMENT
# ==========================================

@app.route("/students")
@login_required
def students():

    search = request.args.get("search", "")

    if search:

        student_list = Student.query.filter(
            Student.full_name.ilike(f"%{search}%")
        ).all()

    else:

        student_list = Student.query.order_by(
            Student.full_name.asc()
        ).all()

    return render_template(
        "students.html",
        students=student_list,
        search=search
    )


@app.route("/add_student", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_student():

    departments = Department.query.order_by(
        Department.name
    ).all()

    if request.method == "POST":

        student = Student(

            reg_no=request.form["reg_no"],

            full_name=request.form["full_name"],

            email=request.form["email"],

            gender=request.form["gender"],

            phone=request.form["phone"],

            date_of_birth=datetime.strptime(
                request.form["date_of_birth"],
                "%Y-%m-%d"
            ).date(),

            address=request.form["address"],

            department_id=request.form["department_id"],

            year_of_study=request.form["year_of_study"],

            semester=request.form["semester"],

            status=request.form["status"]

        )

        db.session.add(student)

        db.session.commit()

        flash(
            "Student added successfully.",
            "success"
        )

        return redirect(url_for("students"))

    return render_template(
        "add_student.html",
        departments=departments
    )


@app.route("/edit_student/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_student(id):

    student = Student.query.get_or_404(id)

    departments = Department.query.order_by(
        Department.name
    ).all()

    if request.method == "POST":

        student.reg_no = request.form["reg_no"]

        student.full_name = request.form["full_name"]

        student.email = request.form["email"]

        student.gender = request.form["gender"]

        student.phone = request.form["phone"]

        student.date_of_birth = datetime.strptime(
            request.form["date_of_birth"],
            "%Y-%m-%d"
        ).date()

        student.address = request.form["address"]

        student.department_id = request.form["department_id"]

        student.year_of_study = request.form["year_of_study"]

        student.semester = request.form["semester"]

        student.status = request.form["status"]

        db.session.commit()

        flash(
            "Student updated successfully.",
            "success"
        )

        return redirect(url_for("students"))

    return render_template(
        "edit_student.html",
        student=student,
        departments=departments
    )


@app.route("/delete_student/<int:id>")
@login_required
@role_required("admin")
def delete_student(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)

    db.session.commit()

    flash(
        "Student deleted successfully.",
        "success"
    )

    return redirect(url_for("students"))


@app.route("/student/<int:id>")
@login_required
def student_profile(id):

    student = Student.query.get_or_404(id)

    registrations = CourseRegistration.query.filter_by(
        student_id=id
    ).all()

    results = Result.query.filter_by(
        student_id=id
    ).all()

    attendance = Attendance.query.filter_by(
        student_id=id
    ).all()

    payments = Payment.query.filter_by(
        student_id=id
    ).all()

    transcript = Transcript.query.filter_by(
        student_id=id
    ).first()

    return render_template(
        "student_profile.html",
        student=student,
        registrations=registrations,
        results=results,
        attendance=attendance,
        payments=payments,
        transcript=transcript
    )
# ==========================================
# PROGRAMME MANAGEMENT
# ==========================================

@app.route("/programmes")
@login_required
def programmes():
    programme_list = Programme.query.order_by(
        Programme.name.asc()
    ).all()

    return render_template(
        "programmes.html",
        programmes=programme_list
    )
# ==========================================
# DEPARTMENT MANAGEMENT
# ==========================================

@app.route("/departments")
@login_required
def departments():

    department_list = Department.query.order_by(
        Department.name.asc()
    ).all()

    return render_template(
        "departments.html",
        departments=department_list
    )


@app.route("/add_department", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_department():

    if request.method == "POST":

        department = Department(

            code=request.form["code"],

            name=request.form["name"],

            hod=request.form["hod"],

            description=request.form["description"]

        )

        db.session.add(department)

        db.session.commit()

        flash(
            "Department added successfully.",
            "success"
        )

        return redirect(url_for("departments"))

    return render_template("add_department.html")


@app.route("/edit_department/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_department(id):

    department = Department.query.get_or_404(id)

    if request.method == "POST":

        department.code = request.form["code"]

        department.name = request.form["name"]

        department.hod = request.form["hod"]

        department.description = request.form["description"]

        db.session.commit()

        flash(
            "Department updated successfully.",
            "success"
        )

        return redirect(url_for("departments"))

    return render_template(
        "edit_department.html",
        department=department
    )


@app.route("/delete_department/<int:id>")
@login_required
@role_required("admin")
def delete_department(id):

    department = Department.query.get_or_404(id)

    db.session.delete(department)

    db.session.commit()

    flash(
        "Department deleted successfully.",
        "success"
    )

    return redirect(url_for("departments"))


# ==========================================
# LECTURER MANAGEMENT
# ==========================================

@app.route("/lecturers")
@login_required
def lecturers():

    lecturer_list = Lecturer.query.order_by(
        Lecturer.full_name.asc()
    ).all()

    return render_template(
        "lecturers.html",
        lecturers=lecturer_list
    )


@app.route("/add_lecturer", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_lecturer():

    departments = Department.query.order_by(
        Department.name.asc()
    ).all()

    if request.method == "POST":

        lecturer = Lecturer(

            staff_no=request.form["staff_no"],

            full_name=request.form["full_name"],

            email=request.form["email"],

            phone=request.form["phone"],

            qualification=request.form["qualification"],

            department_id=request.form["department_id"]

        )

        db.session.add(lecturer)

        db.session.commit()

        flash(
            "Lecturer added successfully.",
            "success"
        )

        return redirect(url_for("lecturers"))

    return render_template(
        "add_lecturer.html",
        departments=departments
    )


@app.route("/edit_lecturer/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_lecturer(id):

    lecturer = Lecturer.query.get_or_404(id)

    departments = Department.query.order_by(
        Department.name.asc()
    ).all()

    if request.method == "POST":

        lecturer.staff_no = request.form["staff_no"]

        lecturer.full_name = request.form["full_name"]

        lecturer.email = request.form["email"]

        lecturer.phone = request.form["phone"]

        lecturer.qualification = request.form["qualification"]

        lecturer.department_id = request.form["department_id"]

        db.session.commit()

        flash(
            "Lecturer updated successfully.",
            "success"
        )

        return redirect(url_for("lecturers"))

    return render_template(
        "edit_lecturer.html",
        lecturer=lecturer,
        departments=departments
    )


@app.route("/delete_lecturer/<int:id>")
@login_required
@role_required("admin")
def delete_lecturer(id):

    lecturer = Lecturer.query.get_or_404(id)

    db.session.delete(lecturer)

    db.session.commit()

    flash(
        "Lecturer deleted successfully.",
        "success"
    )

    return redirect(url_for("lecturers"))


@app.route("/lecturer/<int:id>")
@login_required
def lecturer_profile(id):

    lecturer = Lecturer.query.get_or_404(id)

    courses = Course.query.filter_by(
        lecturer_id=id
    ).all()

    materials = LearningMaterial.query.filter_by(
        lecturer_id=id
    ).all()

    return render_template(
        "lecturer_profile.html",
        lecturer=lecturer,
        courses=courses,
        materials=materials
    )
# ==========================================
# COURSE MANAGEMENT
# ==========================================

@app.route("/courses")
@login_required
def courses():

    course_list = Course.query.order_by(
        Course.code.asc()
    ).all()

    return render_template(
        "courses.html",
        courses=course_list
    )


@app.route("/add_course", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_course():

    departments = Department.query.order_by(
        Department.name
    ).all()

    lecturers = Lecturer.query.order_by(
        Lecturer.full_name
    ).all()

    if request.method == "POST":

        course = Course(

            code=request.form["code"],

            title=request.form["title"],

            description=request.form["description"],

            credit_hours=request.form["credit_hours"],

            semester=request.form["semester"],

            level=request.form["level"],

            department_id=request.form["department_id"],

            lecturer_id=request.form["lecturer_id"]

        )

        db.session.add(course)

        db.session.commit()

        flash(
            "Course added successfully.",
            "success"
        )

        return redirect(url_for("courses"))

    return render_template(
        "add_course.html",
        departments=departments,
        lecturers=lecturers
    )


@app.route("/edit_course/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_course(id):

    course = Course.query.get_or_404(id)

    departments = Department.query.order_by(
        Department.name
    ).all()

    lecturers = Lecturer.query.order_by(
        Lecturer.full_name
    ).all()

    if request.method == "POST":

        course.code = request.form["code"]

        course.title = request.form["title"]

        course.description = request.form["description"]

        course.credit_hours = request.form["credit_hours"]

        course.semester = request.form["semester"]

        course.level = request.form["level"]

        course.department_id = request.form["department_id"]

        course.lecturer_id = request.form["lecturer_id"]

        db.session.commit()

        flash(
            "Course updated successfully.",
            "success"
        )

        return redirect(url_for("courses"))

    return render_template(
        "edit_course.html",
        course=course,
        departments=departments,
        lecturers=lecturers
    )


@app.route("/delete_course/<int:id>")
@login_required
@role_required("admin")
def delete_course(id):

    course = Course.query.get_or_404(id)

    db.session.delete(course)

    db.session.commit()

    flash(
        "Course deleted successfully.",
        "success"
    )

    return redirect(url_for("courses"))


# ==========================================
# COURSE REGISTRATION
# ==========================================

@app.route("/course_registration")
@login_required
def course_registration():

    registrations = CourseRegistration.query.all()

    return render_template(
        "course_registration.html",
        registrations=registrations
    )


@app.route("/register_course", methods=["GET", "POST"])
@login_required
def register_course():

    students = Student.query.order_by(
        Student.full_name
    ).all()

    courses = Course.query.order_by(
        Course.code
    ).all()

    if request.method == "POST":

        registration = CourseRegistration(

            student_id=request.form["student_id"],

            course_id=request.form["course_id"],

            academic_year=request.form["academic_year"],

            semester=request.form["semester"]

        )

        db.session.add(registration)

        db.session.commit()

        flash(
            "Course registered successfully.",
            "success"
        )

        return redirect(
            url_for("course_registration")
        )

    return render_template(
        "register_course.html",
        students=students,
        courses=courses
    )


@app.route("/drop_course/<int:id>")
@login_required
def drop_course(id):

    registration = CourseRegistration.query.get_or_404(id)

    db.session.delete(registration)

    db.session.commit()

    flash(
        "Course dropped successfully.",
        "success"
    )

    return redirect(
        url_for("course_registration")
    )


@app.route("/student_courses/<int:student_id>")
@login_required
def student_courses(student_id):

    student = Student.query.get_or_404(student_id)

    registrations = CourseRegistration.query.filter_by(
        student_id=student.id
    ).all()

    return render_template(
        "student_courses.html",
        student=student,
        registrations=registrations
    )
# ==========================================
# ATTENDANCE MANAGEMENT
# ==========================================

@app.route("/attendance")
@login_required
def attendance():

    attendance_records = Attendance.query.order_by(
        Attendance.date.desc()
    ).all()

    return render_template(
        "attendance.html",
        attendance=attendance_records
    )


@app.route("/take_attendance", methods=["GET", "POST"])
@login_required
@role_required("admin", "lecturer")
def take_attendance():

    students = Student.query.order_by(
        Student.full_name
    ).all()

    courses = Course.query.order_by(
        Course.code
    ).all()

    if request.method == "POST":

        course_id = request.form["course_id"]

        attendance_date = datetime.strptime(
            request.form["date"],
            "%Y-%m-%d"
        ).date()

        present_students = request.form.getlist(
            "present_students"
        )

        for student in students:

            status = (
                "Present"
                if str(student.id) in present_students
                else "Absent"
            )

            record = Attendance(
                student_id=student.id,
                course_id=course_id,
                date=attendance_date,
                status=status
            )

            db.session.add(record)

        db.session.commit()

        flash(
            "Attendance saved successfully.",
            "success"
        )

        return redirect(url_for("attendance"))

    return render_template(
        "take_attendance.html",
        students=students,
        courses=courses
    )


# ==========================================
# REPORTS
# ==========================================

@app.route("/reports")
@login_required
def reports():
    return render_template("reports.html")


# ==========================================
# RESULT MANAGEMENT
# ==========================================

@app.route("/results")
@login_required
def results():

    result_list = Result.query.all()

    return render_template(
        "results.html",
        results=result_list
    )


@app.route("/add_result", methods=["GET", "POST"])
@login_required
@role_required("admin", "lecturer")
def add_result():

    students = Student.query.order_by(
        Student.full_name
    ).all()

    courses = Course.query.order_by(
        Course.code
    ).all()

    if request.method == "POST":

        assignment = float(request.form["assignment"])

        quiz = float(request.form["quiz"])

        exam = float(request.form["exam"])

        total = assignment + quiz + exam

        if total >= 80:
            grade = "A"
            gpa = 4.0

        elif total >= 70:
            grade = "B"
            gpa = 3.0

        elif total >= 60:
            grade = "C"
            gpa = 2.0

        elif total >= 50:
            grade = "D"
            gpa = 1.0

        else:
            grade = "F"
            gpa = 0.0

        result = Result(

            student_id=request.form["student_id"],

            course_id=request.form["course_id"],

            assignment=assignment,

            quiz=quiz,

            exam=exam,

            total=total,

            grade=grade,

            gpa=gpa,

            semester=request.form["semester"],

            academic_year=request.form["academic_year"]

        )

        db.session.add(result)

        db.session.commit()

        flash(
            "Result added successfully.",
            "success"
        )

        return redirect(url_for("results"))

    return render_template(
        "add_result.html",
        students=students,
        courses=courses
    )


@app.route("/delete_result/<int:id>")
@login_required
@role_required("admin")
def delete_result(id):

    result = Result.query.get_or_404(id)

    db.session.delete(result)

    db.session.commit()

    flash(
        "Result deleted successfully.",
        "success"
    )

    return redirect(url_for("results"))


# ==========================================
# TRANSCRIPT
# ==========================================

@app.route("/transcript/<int:student_id>")
@login_required
def transcript(student_id):

    student = Student.query.get_or_404(student_id)

    results = Result.query.filter_by(
        student_id=student.id
    ).all()

    total_points = 0

    total_credits = 0

    for result in results:

        if result.course:

            credits = result.course.credit_hours

            total_points += result.gpa * credits

            total_credits += credits

    cgpa = 0

    if total_credits > 0:

        cgpa = round(
            total_points / total_credits,
            2
        )

    transcript = Transcript.query.filter_by(
        student_id=student.id
    ).first()

    if transcript is None:

        transcript = Transcript(
            student_id=student.id
        )

        db.session.add(transcript)

    transcript.cgpa = cgpa

    transcript.total_credits = total_credits

    if cgpa >= 3.6:
        transcript.classification = "First Class"

    elif cgpa >= 3.0:
        transcript.classification = "Second Class Upper"

    elif cgpa >= 2.0:
        transcript.classification = "Second Class Lower"

    elif cgpa >= 1.0:
        transcript.classification = "Pass"

    else:
        transcript.classification = "Fail"

    db.session.commit()

    return render_template(
        "transcript.html",
        student=student,
        transcript=transcript,
        results=results
    )
# ==========================================
# LEARNING MATERIALS
# ==========================================

@app.route("/learning_materials")
@login_required
def learning_materials():

    materials = LearningMaterial.query.order_by(
        LearningMaterial.uploaded_at.desc()
    ).all()

    return render_template(
        "learning_materials.html",
        materials=materials
    )


@app.route("/add_learning_material", methods=["GET", "POST"])
@login_required
@role_required("admin", "lecturer")
def add_learning_material():

    courses = Course.query.order_by(
        Course.code
    ).all()

    lecturers = Lecturer.query.order_by(
        Lecturer.full_name
    ).all()

    if request.method == "POST":

        material = LearningMaterial(

            course_id=request.form["course_id"],

            lecturer_id=request.form["lecturer_id"],

            title=request.form["title"],

            description=request.form["description"],

            file_name=request.form["file_name"],

            file_path=request.form["file_path"]

        )

        db.session.add(material)

        db.session.commit()

        flash(
            "Learning material uploaded successfully.",
            "success"
        )

        return redirect(
            url_for("learning_materials")
        )

    return render_template(
        "add_learning_material.html",
        courses=courses,
        lecturers=lecturers
    )


# ==========================================
# ASSIGNMENTS
# ==========================================

@app.route("/assignments")
@login_required
def assignments():

    assignment_list = Assignment.query.order_by(
        Assignment.created_at.desc()
    ).all()

    return render_template(
        "assignments.html",
        assignments=assignment_list
    )


@app.route("/add_assignment", methods=["GET", "POST"])
@login_required
@role_required("admin", "lecturer")
def add_assignment():

    courses = Course.query.order_by(
        Course.code
    ).all()

    if request.method == "POST":

        assignment = Assignment(

            course_id=request.form["course_id"],

            title=request.form["title"],

            instructions=request.form["instructions"],

            due_date=datetime.strptime(
                request.form["due_date"],
                "%Y-%m-%d"
            ).date(),

            max_marks=request.form["max_marks"]

        )

        db.session.add(assignment)

        db.session.commit()

        flash(
            "Assignment created successfully.",
            "success"
        )

        return redirect(url_for("assignments"))

    return render_template(
        "add_assignment.html",
        courses=courses
    )


# ==========================================
# ASSIGNMENT SUBMISSION
# ==========================================

@app.route("/submit_assignment/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("student")
def submit_assignment(id):

    assignment = Assignment.query.get_or_404(id)

    if request.method == "POST":

        submission = AssignmentSubmission(

            assignment_id=id,

            student_id=request.form["student_id"],

            file_path=request.form["file_path"]

        )

        db.session.add(submission)

        db.session.commit()

        flash(
            "Assignment submitted successfully.",
            "success"
        )

        return redirect(url_for("assignments"))

    return render_template(
        "submit_assignment.html",
        assignment=assignment
    )


# ==========================================
# QUIZZES
# ==========================================

@app.route("/quizzes")
@login_required
def quizzes():

    quiz_list = Quiz.query.order_by(
        Quiz.created_at.desc()
    ).all()

    return render_template(
        "quizzes.html",
        quizzes=quiz_list
    )


@app.route("/add_quiz", methods=["GET", "POST"])
@login_required
@role_required("admin", "lecturer")
def add_quiz():

    courses = Course.query.order_by(
        Course.code
    ).all()

    if request.method == "POST":

        quiz = Quiz(

            course_id=request.form["course_id"],

            title=request.form["title"],

            instructions=request.form["instructions"],

            duration=request.form["duration"],

            total_marks=request.form["total_marks"]

        )

        db.session.add(quiz)

        db.session.commit()

        flash(
            "Quiz created successfully.",
            "success"
        )

        return redirect(url_for("quizzes"))

    return render_template(
        "add_quiz.html",
        courses=courses
    )


@app.route("/take_quiz/<int:id>")
@login_required
@role_required("student")
def take_quiz(id):

    quiz = Quiz.query.get_or_404(id)

    questions = QuizQuestion.query.filter_by(
        quiz_id=id
    ).all()

    return render_template(
        "take_quiz.html",
        quiz=quiz,
        questions=questions
    )


# ==========================================
# ONLINE EXAMS
# ==========================================

@app.route("/exams")
@login_required
def exams():

    exam_list = Exam.query.order_by(
        Exam.created_at.desc()
    ).all()

    return render_template(
        "exams.html",
        exams=exam_list
    )


@app.route("/add_exam", methods=["GET", "POST"])
@login_required
@role_required("admin", "lecturer")
def add_exam():

    courses = Course.query.order_by(
        Course.code
    ).all()

    if request.method == "POST":

        exam = Exam(

            course_id=request.form["course_id"],

            title=request.form["title"],

            instructions=request.form["instructions"],

            duration=request.form["duration"],

            total_marks=request.form["total_marks"]

        )

        db.session.add(exam)

        db.session.commit()

        flash(
            "Exam created successfully.",
            "success"
        )

        return redirect(url_for("exams"))

    return render_template(
        "add_exam.html",
        courses=courses
    )


@app.route("/take_exam/<int:id>")
@login_required
@role_required("student")
def take_exam(id):

    exam = Exam.query.get_or_404(id)

    questions = ExamQuestion.query.filter_by(
        exam_id=id
    ).all()

    return render_template(
        "take_exam.html",
        exam=exam,
        questions=questions
    )
# ==========================================
# DISCUSSION FORUM
# ==========================================

@app.route("/forum")
@login_required
def forum():

    posts = DiscussionPost.query.order_by(
        DiscussionPost.created_at.desc()
    ).all()

    return render_template(
        "forum.html",
        posts=posts
    )


@app.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():

    if request.method == "POST":

        post = DiscussionPost(

            title=request.form["title"],

            content=request.form["content"],

            author=current_user.full_name

        )

        db.session.add(post)

        db.session.commit()

        flash(
            "Discussion posted successfully.",
            "success"
        )

        return redirect(url_for("forum"))

    return render_template("create_post.html")


@app.route("/reply/<int:post_id>", methods=["POST"])
@login_required
def reply(post_id):

    reply = DiscussionReply(

        post_id=post_id,

        author=current_user.full_name,

        content=request.form["content"]

    )

    db.session.add(reply)

    db.session.commit()

    flash(
        "Reply added successfully.",
        "success"
    )

    return redirect(url_for("forum"))


# ==========================================
# ANNOUNCEMENTS
# ==========================================

@app.route("/announcements")
@login_required
def announcements():

    announcements = Announcement.query.order_by(
        Announcement.created_at.desc()
    ).all()

    return render_template(
        "announcements.html",
        announcements=announcements
    )


@app.route("/add_announcement", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_announcement():

    if request.method == "POST":

        announcement = Announcement(

            title=request.form["title"],

            message=request.form["message"],

            posted_by=current_user.full_name

        )

        db.session.add(announcement)

        db.session.commit()

        flash(
            "Announcement published.",
            "success"
        )

        return redirect(url_for("announcements"))

    return render_template("add_announcement.html")


# ==========================================
# NOTIFICATIONS
# ==========================================

@app.route("/notifications")
@login_required
def notifications():

    notifications = Notification.query.order_by(
        Notification.created_at.desc()
    ).all()

    return render_template(
        "notifications.html",
        notifications=notifications
    )


@app.route("/add_notification", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_notification():

    if request.method == "POST":

        notification = Notification(

            title=request.form["title"],

            message=request.form["message"],

            recipient=request.form["recipient"]

        )

        db.session.add(notification)

        db.session.commit()

        flash(
            "Notification sent successfully.",
            "success"
        )

        return redirect(url_for("notifications"))

    return render_template("add_notification.html")


# ==========================================
# ACADEMIC CALENDAR
# ==========================================

@app.route("/academic_calendar")
@login_required
def academic_calendar():

    events = AcademicCalendar.query.order_by(
        AcademicCalendar.start_date
    ).all()

    return render_template(
        "academic_calendar.html",
        events=events
    )


@app.route("/add_event", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_event():

    if request.method == "POST":

        event = AcademicCalendar(

            title=request.form["title"],

            category=request.form["category"],

            description=request.form["description"],

            start_date=datetime.strptime(
                request.form["start_date"],
                "%Y-%m-%d"
            ).date(),

            end_date=datetime.strptime(
                request.form["end_date"],
                "%Y-%m-%d"
            ).date()

        )

        db.session.add(event)

        db.session.commit()

        flash(
            "Academic event added.",
            "success"
        )

        return redirect(url_for("academic_calendar"))

    return render_template("add_event.html")


# ==========================================
# DIGITAL LIBRARY
# ==========================================

@app.route("/library")
@login_required
def library():

    books = LibraryBook.query.order_by(
        LibraryBook.title
    ).all()

    return render_template(
        "library.html",
        books=books
    )


@app.route("/add_book", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_book():

    if request.method == "POST":

        book = LibraryBook(

            title=request.form["title"],

            author=request.form["author"],

            category=request.form["category"],

            isbn=request.form["isbn"],

            copies=request.form["copies"],

            description=request.form["description"]

        )

        db.session.add(book)

        db.session.commit()

        flash(
            "Book added successfully.",
            "success"
        )

        return redirect(url_for("library"))

    return render_template("add_book.html")


# ==========================================
# FEES & PAYMENTS
# ==========================================

@app.route("/fees")
@login_required
def fees():

    payments = Payment.query.order_by(
        Payment.payment_date.desc()
    ).all()

    return render_template(
        "fees.html",
        payments=payments
    )


@app.route("/add_payment", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_payment():

    students = Student.query.order_by(
        Student.full_name
    ).all()

    if request.method == "POST":

        payment = Payment(

            student_id=request.form["student_id"],

            amount=request.form["amount"],

            semester=request.form["semester"],

            payment_method=request.form["payment_method"],

            reference=request.form["reference"]

        )

        db.session.add(payment)

        db.session.commit()

        flash(
            "Payment recorded successfully.",
            "success"
        )

        return redirect(url_for("fees"))

    return render_template(
        "add_payment.html",
        students=students
    )


# ==========================================
# SYSTEM SETTINGS
# ==========================================

@app.route("/settings", methods=["GET", "POST"])
@login_required
@role_required("admin")
def settings():

    settings = SystemSetting.query.first()

    if settings is None:

        settings = SystemSetting()

        db.session.add(settings)

        db.session.commit()

    if request.method == "POST":

        settings.institution_name = request.form["institution_name"]

        settings.institution_email = request.form["institution_email"]

        settings.institution_phone = request.form["institution_phone"]

        settings.institution_address = request.form["institution_address"]

        settings.academic_year = request.form["academic_year"]

        settings.current_semester = request.form["current_semester"]

        db.session.commit()

        flash(
            "System settings updated.",
            "success"
        )

        return redirect(url_for("settings"))

    return render_template(
        "settings.html",
        settings=settings
    )