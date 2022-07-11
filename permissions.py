from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminWritePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return False  # todo for admin must be true


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser  # todo add is_admin later
