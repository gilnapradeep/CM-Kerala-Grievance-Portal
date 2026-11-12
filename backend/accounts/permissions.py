
from rest_framework.permissions import BasePermission


class IsCMOAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'CMO_ADMIN'
        )


class IsDepartmentOfficer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'OFFICER'
        )


class IsCMOOrOfficer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ['CMO_ADMIN', 'OFFICER']
        )
