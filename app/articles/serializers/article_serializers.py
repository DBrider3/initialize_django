# System
from rest_framework import serializers

# Project
from app.articles.models import Article


class WriteArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField(allow_blank=True, required=False)


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.email

    class Meta:
        model = Article
        fields = "__all__"
