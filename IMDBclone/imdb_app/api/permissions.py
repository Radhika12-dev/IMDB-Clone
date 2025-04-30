#This file contains all the custom permissions we created for our API.

from rest_framework import permissions

class AdminOrReadOnly(permissions.IsAdminUser):
    """
    Custom permission to only allow admin users to view and edit.
    """
    def has_permission(self, request, view):
        #we are overriding the has_permission method to allow only admin users to edit and all users to view the data
        admin_permission = bool(request.user and request.user.is_staff)
        return admin_permission or request.method == "GET"

class ReviewUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own reviews.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the review
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.review_user == request.user