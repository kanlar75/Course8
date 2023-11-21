from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """ Проверяет к своей ли привычке запрашивает доступ пользователь """

    message = 'Вы не являетесь владельцем!'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user or request.user.is_superuser:
            return True
        return False
