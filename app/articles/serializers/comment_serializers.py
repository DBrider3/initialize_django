# System
from rest_framework import serializers

# Project
from app.articles.models import Comment


class WriteCommentSerializer(serializers.Serializer):
    content = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.email

    class Meta:
        model = Comment
        exclude = ["article"]
