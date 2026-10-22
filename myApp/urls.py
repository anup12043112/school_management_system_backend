from django.urls import path, include
from .views import UserView, TeacherView, StudentView, ParentView, SectionView, SubjectView, TeachingAssignmentView, AttendanceView, MarksView, NoticeView, MeView, MarksSummary
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register("users", UserView, basename="user")
router.register("teachers", TeacherView, basename="teacher")
router.register("students", StudentView, basename="student")
router.register("parents", ParentView, basename="parent")
router.register("sections", SectionView, basename="section")
router.register("subjects", SubjectView, basename="subject")
router.register("teaching-assignments", TeachingAssignmentView, basename="teaching-assignment")
router.register("attendance", AttendanceView, basename="attendance")
router.register("marks", MarksView, basename="marks")
router.register("notices", NoticeView, basename="notice")
router.register("marks-summary", MarksSummary, basename="marksSummary")

urlpatterns = [
    path("", include(router.urls)),
    path("access/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("auth/me/", MeView.as_view()),
]