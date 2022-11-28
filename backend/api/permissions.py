from rest_framework import (
    permissions,
)


def is_staff(request):
    return (
        request.user.is_superuser
        or request.user.is_admin
        or request.user.is_staff
    )


class OwnerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.owner == request.user
            or is_staff(request)
        )


class IsStaffOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_staff(request)


class StaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or is_staff(request)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or is_staff(request)
        )


class CreateOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or is_staff(request)
        )

