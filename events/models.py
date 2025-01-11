from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.utils import timezone
from django.core.validators import MinValueValidator

class User(AbstractUser):
    is_host = models.BooleanField(default=False)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    attendees = models.ManyToManyField(User, related_name='registered_events', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events', null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def is_past_event(self):
        return self.date_time < timezone.now()

    def is_full(self):
        return self.attendees.count() >= self.capacity

    def __str__(self):
        return self.title

class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.event.title}'