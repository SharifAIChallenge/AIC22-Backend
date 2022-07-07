from rest_framework.permissions import BasePermission


class ProfileComplete(BasePermission):
    message = "complete your profile first"

    def has_permission(self, request, view):
        return request.user.profile.is_complete
