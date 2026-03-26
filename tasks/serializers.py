from rest_framework import serializers
from .models import Task, Category, Tag
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    #Lectura (GET)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True,read_only=True)

    #Para escritura (POST, PUT, PATCH)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, source='tags', write_only=True)


    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at', 'category', 'tags','category_id','tag_ids']
        read_only_fields = ['created_at','user']

    # VALIDACIÓN 1 (campo titulo)
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "El título debe tener al menos 3 caracteres"
            )
        return value

    # VALIDACIÓN 2 (validación tareas completadas deben tener descripción)
    def validate(self, data):
        if data.get('status') == 'completed' and not data.get('description'):
            raise serializers.ValidationError(
                "Las tareas completadas deben tener descripción"
            )
        return data