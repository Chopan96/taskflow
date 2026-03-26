from .models import Task, Category, Tag
from rest_framework import viewsets, permissions, generics
from .serializers import TaskSerializer, CategorySerializer, TagSerializer, UserSerializer
from django.contrib.auth.models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] # Permitir registro sin autenticación

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated] # modificar según necesidades

    def get_queryset(self):
        #Usar esto cuando se utilice usuario autenticado:
        queryset = Task.objects.filter(user=self.request.user) 
        #queryset = Task.objects.all()
        # Filtro por estado
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Filtro por categoría
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__id=category)

        # Filtro por tag
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__id=tag)

        return queryset

    def perform_create(self, serializer):
        # Cambiar a esto cuando se utilice usuario autenticado:
        serializer.save(user=self.request.user)
        #serializer.save(user_id=1)  # usuario fijo temporal

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny] # modificar según necesidades

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny] # modificar según necesidades

