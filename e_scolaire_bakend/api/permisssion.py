from rest_framework.permissions import BasePermission
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'Admin'
    
class IsEtudiant(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'Etudiant'