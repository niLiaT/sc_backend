from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from .models import User, Article, Comment
from .serializers import UserSerializer, ArticleSerializer, CommentSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

@api_view(['POST'])
def get_comments(request):
    user_data = JSONParser().parse(request)
    comments = Comment.objects.filter(poster_id=user_data['id'])
    comment_serializer = CommentSerializer(comments, many=True)
    return JsonResponse(comment_serializer.data, safe=False)

@api_view(['POST'])
def get_article(request):
    article_data = JSONParser().parse(request)
    article = Article.objects.get(id=article_data['id'])
    article_serializer = ArticleSerializer(article)
    return JsonResponse(article_serializer.data, safe=False)

@api_view(['POST'])
def get_articles(request):
    user_data = JSONParser().parse(request)
    articles = Article.objects.filter(original_poster_id=user_data['id'])
    article_serializer = ArticleSerializer(articles, many=True)
    return JsonResponse(article_serializer.data, safe=False)