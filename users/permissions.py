from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Permission для модераторов:
    - is_staff=True
    - Может: GET, PUT, PATCH, DELETE (включая чужие продукты)
    - НЕ может: POST
    """
    
    # Разрешенные методы для модератора
    allowed_methods = ['GET', 'PUT', 'PATCH', 'DELETE']
    
    def has_permission(self, request, view):
        # Проверяем аутентификацию и is_staff
        if not request.user or not request.user.is_authenticated:
            return False
        
        if not request.user.is_staff:
            return False
        
        # Проверяем метод
        if request.method == 'POST':
            return False
        
        if request.method not in self.allowed_methods:
            return False
        
        return True
    
    def has_object_permission(self, request, view, obj):
        # Модератор может работать с любым объектом
        return True