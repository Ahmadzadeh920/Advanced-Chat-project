from rest_framework import permissions

from .models import Profile


class IsVerified(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.user.is_verified:
            return True

        # Instance must have an attribute named `owner`.
        else:
            return False
        



class IsProfileCompleted(permissions.BasePermission):
    """
    Custom permission to only allow users with completed profiles to access a view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if  request.user.is_authenticated:
            Profile_obj = Profile.objects.filter(user = request.user)
            if Profile_obj:
                return True
            # Check if the user has a completed profile
            # Adjust this logic based on how you identify a completed profile
        return False
