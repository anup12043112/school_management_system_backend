from django.contrib import admin
from .models import User
from .models import Teacher, Student, Parent, Section, Subject, TeachingAssignment, Attendance, Marks, Notice 

# Register your models here.
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(TeachingAssignment)
admin.site.register(Attendance)
admin.site.register(Marks)
admin.site.register(Notice)