from rest_framework import serializers
from .models import Node, Link

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'

class GraphSerializer(serializers.Serializer):
    nodes = NodeSerializer(many=True)
    links = LinkSerializer(many=True)