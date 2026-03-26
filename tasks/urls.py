from rest_framework import routers
from .api import TaskViewSet, CategoryViewSet, TagViewSet, RegisterView
from django.urls import path, include

router = routers.DefaultRouter()

router.register('api/tasks', TaskViewSet, 'tasks')
router.register('api/categories', CategoryViewSet, 'categories')
router.register('api/tags', TagViewSet, 'tags')

urlpatterns = [
    path('', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
]