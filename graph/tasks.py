from django.db.models import Count
from django.db import IntegrityError

from data_api.models import CommonComment
from .models import Node, Link

def update_models():
    Node.objects.all().delete()
    Link.objects.all().delete()
    top_concurrency = CommonComment.objects.order_by('-weight')[:1000]
    for concurrency in top_concurrency:
        try:
            account1 = Node.objects.create(nodeId=concurrency.account1.id, party='N/A')
        except IntegrityError:
            account1 = Node.objects.get(nodeId=concurrency.account1.id)
        try:
            account2 = Node.objects.create(nodeId=concurrency.account2.id, party='N/A')
        except IntegrityError:
            account2 = Node.objects.get(nodeId=concurrency.account2.id)

        comments = concurrency.account1.replies.all() | concurrency.account2.replies.all()
        group = comments.all().values('article').annotate(number=Count('article')).order_by('number')

        common_rate = concurrency.weight / len(group)

        if common_rate > 0.3:
            Link.objects.create(source=account1, target=account2, value=concurrency.weight / len(group))