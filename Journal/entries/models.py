from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Entries model
class Entry(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

# Tag model
class Tag(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
# EntryReminder model
class EntryReminder(models.Model):
    users = models.ForeignKey(Entry, on_delete=models.CASCADE)
    remind_at = models.DateTimeField()
    message = models.TextField()

    def __str__(self):
        return self.message
