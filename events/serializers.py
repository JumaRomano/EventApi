from rest_framework import serializers
from .models import Event, User, Category, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_host']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date_time', 'location', 'organizer', 'capacity', 'attendees', 'category', 'created_date']
        read_only_fields = ['created_date', 'organizer']

    def validate(self, data):
        if data['date_time'] < timezone.now():
            raise serializers.ValidationError("Event date and time must be in the future.")
        if data['capacity'] <= 0:
            raise serializers.ValidationError("Capacity must be greater than zero.")
        return data

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'event', 'user', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)