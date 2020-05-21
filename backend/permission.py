from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class HasTemplate(BasePermission):  # Zostawiam Wam do wglądu pisanie permisji do API
    def has_permission(self, request, view):
        pass
