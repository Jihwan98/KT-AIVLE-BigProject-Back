from rest_framework import permissions

class IsVetAuthenticated(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):        
        # 요청자의 is_vet return (request.user.is_vet) 
        return request.user.is_vet

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 요청자(request.userid)가 객체(Blog)의 user와 동일한지 확인
        return obj.user_id == request.user