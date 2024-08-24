from rest_framework import permissions

class IsProfileCompleted(permissions.BasePermission):
    """
    Custom permission to only allow users with completed profiles to access a view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        profile_obj = Pr
        if request.user.is_authenticated:
            # Check if the user has a completed profile
            # Adjust this logic based on how you identify a completed profile
            return request.user.profile.is_completed  # Assuming there's a profile with 'is_completed' field
        return False