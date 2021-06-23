from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'comments', views.get_comments),
    url(r'article', views.get_article),
    url(r'articles', views.get_articles),
]