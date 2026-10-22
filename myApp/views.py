from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from .models import (
    User,
    Teacher,
    Student,
    Parent,
    Section,
    Subject,
    TeachingAssignment,
    Attendance,
    Marks,
    Notice,
)
from .serializers import (
    UserSerializer,
    TeacherSerializer,
    StudentSerializer,
    ParentSerializer,
    SectionSerializer,
    SubjectSerializer,
    TeachingAssignmentSerializer,
    AttendanceSerializer,
    MarksSerializer,
    NoticeSerializer,
)

from rest_framework.permissions import IsAuthenticated, BasePermission, IsAdminUser
from .permissions import (
    ManageTeacher,
    ManageStudent,
    ManageParent,
    ManageTeachingAssignment,
    ManageNotice,
    ManageAttendance,
    ManageMarks,
)


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ["first_name", "last_name", "username"]

    # def get_queryset(self):

    #     return super().get_queryset()


class TeacherView(ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [ManageTeacher]

    filter_backends = [SearchFilter]
    search_fields = [
        "student__user__first_name",
        "student__user__last_name",
        "student__user__username",
    ]

    def get_queryset(self):
        order = self.request.query_params.get("order")
        if order == "name":
            order = "user__first_name"
        elif order == "email":
            order = "email"
        elif order == "dob":
            order = "dob"
        else:
            order = "id"

        role = self.request.user.role
        if role == "admin":
            return Teacher.objects.all().order_by(order)
        if role == "teacher":
            return Teacher.objects.filter(id=self.request.user.teacher.id)
        return Teacher.objects.none()


class StudentView(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [ManageStudent]

    filter_backends = [SearchFilter]
    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__username",
    ]

    def get_queryset(self):
        order = self.request.query_params.get("order")
        section = self.request.query_params.get("section")
        if order == "name":
            order = "user__first_name"
        elif order == "email":
            order = "email"
        elif order == "dob":
            order = "dob"
        else:
            order = "id"

        role = self.request.user.role
        if role in ["admin", "teacher"]:
            queryset = Student.objects.all().order_by(order)
            if section:
                queryset = queryset.filter(section__section=section)
            return queryset

        if role == "student":
            return Student.objects.filter(id=self.request.user.student.id)
        return Student.objects.none()


class ParentView(ModelViewSet):
    serializer_class = ParentSerializer
    permission_classes = [ManageParent]

    filter_backends = [SearchFilter]
    search_fields = [
        "student__user__first_name",
        "student__user__last_name",
        "student__user__username",
    ]

    def get_queryset(self):
        order = self.request.query_params.get("order")
        if order == "name":
            order = "user__first_name"
        elif order == "email":
            order = "email"
        else:
            order = "id"

        role = self.request.user.role
        if role == "admin":
            return Parent.objects.all().order_by(order)
        if role == "parent":
            return Parent.objects.filter(id=self.request.user.parent.id)
        return Parent.objects.none()


class TeacherAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ["admin", "teacher"]

class SectionView(ModelViewSet):
    serializer_class = SectionSerializer
    permission_classes = [TeacherAdminOnly]

    def get_queryset(self):
        if self.request.user.role in ["admin", "teacher"]:
            return Section.objects.all()
        return Section.objects.none()


class SubjectView(ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [TeacherAdminOnly]
    filter_backends = [SearchFilter]
    search_fields = [
        "subject",
    ]

    def get_queryset(self):
        if self.request.user.role in ["admin", "teacher"]:
            return Subject.objects.all()
        return Subject.objects.none()


class TeachingAssignmentView(ModelViewSet):
    serializer_class = TeachingAssignmentSerializer
    permission_classes = [ManageTeachingAssignment]
    filter_backends = [SearchFilter]
    search_fields = [
        "teacher__user__first_name",
        "teacher__user__last_name",
        "teacher__user__username",
    ]

    def get_queryset(self):
        section = self.request.query_params.get("section")
        teacher = self.request.query_params.get("teacher")
        subject = self.request.query_params.get("subject")

        role = self.request.user.role
        if role == "admin":
            queryset = TeachingAssignment.objects.all()
            if section:
                queryset = queryset.filter(section__section=section)
            if teacher:
                queryset = queryset.filter(teacher__user__username=teacher)
            if subject:
                queryset = queryset.filter(subject__subject__iexact=subject)
            return queryset

        if role == "teacher":
            return TeachingAssignment.objects.filter(teacher=self.request.user.teacher)

        return TeachingAssignment.objects.none()

class AttendancePagination(PageNumberPagination):
    page_size = 10

class AttendanceView(ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [ManageAttendance]
    pagination_class = AttendancePagination
    filter_backends = [SearchFilter]
    search_fields = [
        "student__user__first_name",
        "student__user__last_name",
        "student__user__username",
    ]

    def get_queryset(self):
        order = self.request.query_params.get("order")  # for ordering
        section = self.request.query_params.get("section")  # for filtering
        present = self.request.query_params.get("present")  # for filtering

        if order == "name":
            order = "student__user__first_name"
        elif order == "-name":
            order = "-student__user__first_name"
        elif order == "date":
            order = "date"
        else:
            order = "-date"

        role = self.request.user.role
        if role in ["admin", "teacher"]:
            queryset = Attendance.objects.all().order_by(order)
            if section:
                queryset = queryset.filter(student__section__section=section)
            if present:
                if present.lower() == "true":
                    queryset = queryset.filter(attendance=True)
                if present.lower() == "false":
                    queryset = queryset.filter(attendance=False)
            return queryset
        if role == "student":
            return Attendance.objects.filter(student=self.request.user.student)

        return Attendance.objects.none()


class MarksView(ModelViewSet):
    serializer_class = MarksSerializer
    permission_classes = [ManageMarks]
    filter_backends = [SearchFilter]
    pagination_class = AttendancePagination
    
    search_fields = [
        "student__user__first_name",
        "student__user__last_name",
        "student__user__username",
    ]

    def get_queryset(self):
        sec = self.request.query_params.get("section")
        exam = self.request.query_params.get("exam")
        sub = self.request.query_params.get("subject")

        queryset = Marks.objects.all()
        role = self.request.user.role
        if role in ["admin", "teacher"]:
            if sec:
                queryset = queryset.filter(student__section__section = sec)
            if exam: 
                if exam == "1":
                    queryset = queryset.filter(exam = "unit test")
                if exam == "2":
                    queryset = queryset.filter(exam = "mid term exam")
                if exam == "3":
                    queryset = queryset.filter(exam = "annual exam")
            if sub:
                queryset = queryset.filter(subject__subject = sub)
            return queryset
        
        if role == "student":
            return queryset.filter(student=self.request.user.student)
        if role == "parent":
            return queryset.filter(student=self.request.user.parent.children)

        return Marks.objects.none()


class MarksSummary(ModelViewSet):
    serializer_class = MarksSerializer
    filter_backends = [SearchFilter]
    
    search_fields = [
        "student__user__first_name",
        "student__user__username",
    ]

    def get_queryset(self):
        role = self.request.user.role
        if role in ["admin", "teacher"]:
            return Marks.objects.all()
        
        return Marks.objects.none()


class NoticeView(ModelViewSet):
    serializer_class = NoticeSerializer
    queryset = Notice.objects.all()
    permission_classes = [ManageNotice]


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "id": request.user.id,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "username": request.user.username,
                "role": request.user.role,
            }
        )
