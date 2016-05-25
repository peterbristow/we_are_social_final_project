from rest_framework import serializers

from .models import Thread, Posts


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ('id', 'thread', 'comment', 'user', 'created_at')


class ThreadSerializer(serializers.ModelSerializer):

    posts = PostSerializer(many=True)

    class Meta:
        model = Thread
        fields = ('id', 'name', 'user', 'subject', 'created_at', 'posts')
