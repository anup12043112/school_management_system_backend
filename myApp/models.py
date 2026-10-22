from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("teacher", "Teacher"),
        ("student", "Student"),
        ("parent", "Parent"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.user.username 



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    email = models.EmailField()
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    section = models.ForeignKey("Section", on_delete=models.CASCADE, related_name="students")

    def __str__(self):
        return self.user.username 
    


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    children = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="parent")

    def __str__(self):
        return self.user.username 



class Section(models.Model):
    section = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.section


class Subject(models.Model):
    subject = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.subject


class TeachingAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.teacher.user.username} - {self.section.section}"  



class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance")
    attendance = models.BooleanField()
    date = models.DateField()

    def __str__(self):
        return f"{self.student.user.username} - {self.date}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "date"],
                name = "student_attendance" 
            )

        ]


class Marks(models.Model):
    EXAM_CHOICES = [
        ("mid term exam", "MidTerm Exam"),
        ("annual exam", "Annual Exam"),
        ("unit test", "Unit Test"),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    exam = models.CharField(max_length=30, choices=EXAM_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['student', 'subject', 'exam'],
                name = 'unique_student_subject_exam'
            )
        ]

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.subject}"


class Notice(models.Model):
    header = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    posted_by = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.header} -- {self.posted_by}"
