from rest_framework import permissions

class IsHostOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow hosts to edit their events.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.organizer == request.user and request.user.is_authenticated