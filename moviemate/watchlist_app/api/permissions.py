from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
    """
    Custom permission to only allow admins to edit objects.
    Non-admin users can only read objects.
    """

    def has_permission(self, request, view):
        # Allow read-only access for non-authenticated users
        # admin_permission = super().has_permission(request, view) # Using the parent class's method to check if the user is an admin
        # admin_permission = bool(request.user and request.user.is_staff )# Check if the user is authenticated and is an admin
        
        # return request.method == 'GET' or admin_permission
    
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)
    

class IsReviewUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the user who created the review to edit it.
    Non-authenticated users can only read reviews.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only access for non-authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow write access only to the user who created the review
        return obj.review_user == request.user

