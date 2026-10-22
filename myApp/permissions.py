from rest_framework.permissions import BasePermission


class ManageTeacher(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = request.user.role
        action = view.action 
        if action in ["list", "retrieve", "partial_update"]:
            return role in ["admin", "teacher"]
        
        return role == "admin"
    
    def has_object_permission(self, request, view, obj):
        role = request.user.role
        if role == "admin":
            return True
        if role == "teacher":
            return request.user.teacher.id == obj.id
        return False


class ManageStudent(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = request.user.role
        action = view.action 
        if action in ["list", "retrieve"]:
            return role in ["admin", "student", "teacher"]
        if action == "partial_update":
            return role in ["admin", "student"]
        
        return role == "admin"
    
    def has_object_permission(self, request, view, obj):
        role = request.user.role
        if role == "admin" or "teacher":
            return True
        if role == "student":
            return request.user.student.id == obj.id
        return False


class ManageParent(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = request.user.role
        action = view.action 
        if action in ["list", "retrieve", "partial_update"]:
            return role in ["admin", "parent"]
        
        return role == "admin"
    
    def has_object_permission(self, request, view, obj):
        role = request.user.role
        if role == "admin":
            return True
        if role == "parent":
            return request.user.parent.id == obj.id
        return False
    



class ManageTeachingAssignment(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = request.user.role
        action = view.action 
        if action in ['list', 'retrieve']:
            return role in ["teacher", "admin"]
        return role == "admin"
    
    def has_object_permission(self, request, view, obj):
        role = request.user.role
        if role == "admin":
            return True
        if role == "teacher":
            return obj.teacher == request.user.teacher 
        return False
    


class ManageAttendance(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = request.user.role
        action = view.action 
        if action in ["list", "retrieve"]:
            return True
        if action in ["partial_update"]:
            return role in ["admin", "teacher"]

        return role == "admin"
    
    def has_object_permission(self, request, view, obj):
        role = request.user.role
        if role in ["admin", "teacher"]:
            return True
        if role == "student":
            return obj.student == request.user.student
        if role == "parent":
            return obj.student == request.user.parent.children

        return super().has_object_permission(request, view, obj)
    


class ManageMarks(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = request.user.role
        action = view.action 
        if action in ["list", "retrieve"]:
            return True
        if action in ["create", "partial_update"]:
            return role in ["admin", "teacher"]
        
        return role == "admin"
    
    def has_object_permission(self, request, view, obj):
        role = request.user.role
        if role == "admin":
            return True
        if role == "teacher":
            return request.user.teacher.teachingassignment_set.filter(subject=obj.subject).exists()
        if role == "student":
            return obj.student == request.user.student
        if role == "parent":
            return obj.student == request.user.parent.children
        return False



class ManageNotice(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        role = request.user.role
        action = view.action 
        if action in ["list", "retrieve"]:
            return True
        if action == "create":
            return role in ["teacher", "admin"]
        return role == "admin"