from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners or admins of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet or admin.

        if request.user.is_staff:
            return True

        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        else:
            return obj.user == request.user

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to read and edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read and write permissions are only allowed to the owner of the snippet or admin.

        if request.user.is_staff:
            return True

        return obj.user == request.user
