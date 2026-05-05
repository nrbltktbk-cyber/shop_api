from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action
from users.permissions import IsModerator
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        # GET запросы - может любой аутентифицированный
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        
        # POST (создание) - только админы (is_superuser)
        elif self.action == 'create':
            permission_classes = [permissions.IsAdminUser]
        
        # PUT, PATCH, DELETE - модераторы (is_staff, но не создают)
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsModerator]
        
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]