from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if method is a safe method give permissions
        if request.method in permissions.SAFE_METHODS:
            return True
        # if user is superuser give permissions
        if request.user.is_superuser:
            return True
        # if user is owner give permissions
        return obj.owner == request.user
