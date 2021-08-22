from rest_framework.permissions import BasePermission


class IsHume(BasePermission):
    """Permission check to ensure that a user is a HUME."""

    def has_permission(self, request, view):
        return request.user.is_hume
