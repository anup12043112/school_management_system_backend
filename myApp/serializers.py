from rest_framework import serializers
from .models import User, Teacher, Student, Parent, Section, Subject, TeachingAssignment, Attendance, Marks, Notice 


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "role"]


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        write_only = True,
        source = "user"
    )
    class Meta:
        model = Teacher
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()
        role = self.context.get("request").user.role
        if self.instance is not None and role != "admin":
            fields["user"].read_only = True
        return fields


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    section = serializers.SlugRelatedField(slug_field = "section", read_only = True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        write_only = True,
        source = "user"
    )
    section_id = serializers.PrimaryKeyRelatedField(
        queryset = Section.objects.all(),
        write_only = True,
        source = "section"
    )
    class Meta:
        model = Student
        fields = "__all__"
    
    def get_fields(self):
        fields = super().get_fields()
        role = self.context.get("request").user.role
        if self.instance is not None and role != "admin":
            fields["user"].read_only = True
            fields["section"].read_only = True
        return fields
    
    

class ParentSerializer(serializers.ModelSerializer):  
    user = UserSerializer(read_only=True) 
    children = StudentSerializer(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Parent.objects.all(),
        source="user",
        write_only=True
    )
    children_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        source="student",
        write_only=True
    )
    class Meta:
        model = Parent
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()
        role = self.context.get("request").user.role
        if self.instance is not None and role != "admin":
            fields["user"].read_only = True
            fields["children"].read_only = True
        return fields


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class TeachingAssignmentSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only = True)
    subject = SubjectSerializer(read_only = True)
    section = SectionSerializer(read_only = True)
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(),
        source="teacher",
        write_only=True
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source="subject",
        write_only=True
    )
    section_id = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.all(), 
        source="section",
        write_only=True
    )
    
    class Meta:
        model = TeachingAssignment
        fields = "__all__"


class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True) 
    student_id = serializers.PrimaryKeyRelatedField(
        queryset = Student.objects.all(),
        write_only = True,
        source = "student"
    ) 
    class Meta:
        model = Attendance
        fields = "__all__"


class MarksSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only = True)
    subject = SubjectSerializer(read_only = True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),
        source="student",
        write_only=True
    )
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source="subject",
        write_only=True
    )
    class Meta:
        model = Marks
        fields = "__all__" 
    
    def get_fields(self):
        fields = super().get_fields()
        if self.instance is not None:
            fields["student"].read_only = True
            fields["subject"].read_only = True
            fields["total_marks"].read_only = True
            fields["exam"].read_only = True
        return fields


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"

    def get_fields(self):
        fields = super().get_fields()
        if self.instance is not None:
            fields["date"].read_only = True
            fields["posted_by"].read_only = True
        return fields