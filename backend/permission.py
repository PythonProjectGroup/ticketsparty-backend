from rest_framework.permissions import BasePermission,SAFE_METHODS
from backend.models import Inquiry

class IsOwnerProfileOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        '''if request.method in SAFE_METHODS:
            return True'''
        return obj==request.user

class HasTemplate(BasePermission): #Zostawiam Wam do wglądu pisanie permisji do API
    def has_permission(self, request, view):
        pass
