import json

from django.core.serializers import serialize
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from store.models import Product


def say_hello(request):
    # query_set = Product.objects.filter(unit_price__range=(20, 30))
    query_set = Product.objects.filter(Q())
    serialized_data = serialize("json", query_set, use_natural_foreign_keys=True)
    serialized_data = json.loads(serialized_data)

    return JsonResponse(serialized_data, safe=False, status=200)


### querysets examples
# query_set = Product.objects.all()

# query_set.filter().order_by()
# query_set = Product.objects.filter(unit_price__gt=1)
# query_set = Product.objects.filter(unit_price__range=(20, 30))

## Relationships
# query_set = Product.objects.filter(collection__id__range=(1,2,3))

# query_set = Product.objects.filter(title__contains='search_this')
# query_set = Product.objects.filter(title__icontains='search_this')
# query_set = Product.objects.filter(last_update__year=2021)

### 44 Multiple Filters
# Product: inventory < 10 AND price < 20
# query_set = Product.objects.filter(fieldName=val,fieldName2=val2)
# query_set = Product.objects.filter(fieldName=val).filter(fieldName2=val2)
# OR
