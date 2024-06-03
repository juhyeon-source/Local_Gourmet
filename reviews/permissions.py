from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_active
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user