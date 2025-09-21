from rest_framework import serializers
from .models import Entry, Tag, EntryReminder

class EntriesSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True) # Username 
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    class Meta:
        model = Entry
        fields = ['id', 'user', 'title', 'content',  'tags', 'created_at', 'updated_at']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class EntryReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryReminder
        fields = ['id', 'users', 'remind_at', 'message']

