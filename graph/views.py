from rest_framework import viewsets
from rest_framework.response import Response
from collections import namedtuple

from .serializers import GraphSerializer
from .models import Node, Link

# Create your views here.
Graph = namedtuple('Graph', ('nodes', 'links'))

# Create your views here.
class GraphViewSet(viewsets.ViewSet):
    def list(self, requst):
        graph = Graph(
            nodes = Node.objects.all(),
            links = Link.objects.all(),
        )
        serializer = GraphSerializer(graph)
        return Response(serializer.data)
