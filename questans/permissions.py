from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsObjectUserOrReadOnly(BasePermission):
    """
    Custom permission to only allow write access to object's user (owner) or allow read-only requests
    """

    def has_object_permission(self, request, view, obj):
        # READ permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user


class IsObjectUser(BasePermission):
    """
    Custom permission to only allow access to the object's user (owner)
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
