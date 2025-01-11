from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Event, User, Category, Comment
from .serializers import EventSerializer, UserSerializer, CategorySerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user to register

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can manage categories

class EventFilter(filters.FilterSet):
    category = filters.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Event
        fields = ['category']

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def register_for_event(self, request, pk=None):
        event = self.get_object()
        if event.attendees.count() < event.capacity:
            event.attendees.add(request.user)
            return Response({"status": "registered"}, status=status.HTTP_200_OK)
        return Response({"status": "event full"}, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(event__organizer=self.request.user)  # Only allow hosts to see their comments

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically set the user to the logged-in user