from rest_framework.permissions import BasePermission

class IsAuthenticated(BasePermission):
    """
    Custom permission to check for the presence of 'uid' in cookies.
    """
    
    def has_permission(self, request, view):
        # Check if 'uid' is in the request cookies
        return 'uid' in request.COOKIES
