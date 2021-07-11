from django.db import models

from data_api.models import User, Article

# Create your models here.
class Node(models.Model):
    nodeId = models.CharField(max_length=12, primary_key=True)
    party = models.CharField(max_length=10)

class Link(models.Model):
    source = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='out_edge')
    target = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='in_edge')
    value = models.FloatField()