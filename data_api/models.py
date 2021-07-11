from django.db import models

# Create your models here.
class User(models.Model):
    id = models.CharField(max_length=12, primary_key=True)

class Article(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    original_poster = models.ForeignKey('User', related_name='posts', on_delete=models.CASCADE)
    board = models.CharField(max_length=20)
    title = models.CharField(max_length=30)
    date = models.DateField()
    time = models.TimeField()
    ip = models.CharField(max_length=15)
    content = models.TextField()

class Comment(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    poster = models.ForeignKey('User', related_name='replies', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', related_name='discussions', on_delete=models.CASCADE)
    reaction = models.CharField(max_length=1)
    opinion = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    ip = models.CharField(max_length=15)

class CommonComment(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    account1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='common_user1')
    account2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='common_user2')
    weight = models.IntegerField(default=0)