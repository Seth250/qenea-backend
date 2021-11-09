from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsObjectUserOrReadOnly(BasePermission):
    """
    Custom permission to only allow the object's user (owner) to modify it 
    """

    def has_object_permission(self, request, view, obj):
        # READ permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
