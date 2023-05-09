import json

from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize
from django.db import transaction
from django.db.models import F, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from store.models import Order, OrderItem, Product
from tags.models import TaggedItem


# @transaction.atomic()
def say_hello(request):
    print("gi")  # with transaction.atomic():
    #     # ...actions
    # serialized_data = serialize("json", query_set, use_natural_foreign_keys=True)
    # serialized_data = json.loads(serialized_data)

    # return JsonResponse(serialized_data, safe=False, status=200)


### querysets examples
# query_set = Product.objects.all()
# query_set = Product.objects.all()[:5] => Limit = 5
# query_set = Product.objects.all()[5:10] => Limit = 5 , skip/offset=5

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
# query_set = Product.objects.filter( Q(fieldName=val) | Q(fieldName=val) )
# | => OR
# & => AND
# & ~ => AND NOT

### 45 Reference
# query_set = Product.objects.filter(inventory=F("collection__id"))
# query_set = Product.objects.filter(inventory=F("unit_price"))


##
# product_ids = OrderItem.objects.values("product_id").distinct()
# query_set = (Product.objects.filter(id__in=product_ids).order_by("title"))
# .order_by("-dateField"))

# values()
# Only()  # method can make a query call to data base


# select_related(foreignField) & prefetch_related (Many to Many)
# select_related() // Will preload collection
# query_set = Product.objects.select_related('collection').all()
# query_set = Product.objects.select_related('collection__some OtherCollectionFieldID').all()

# query_set = Product.objects.prefetch_related('promotions').all()

# query_set = Order.objects.select_related('collection').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]

# Aggregate

# -------------
# Generic relationship
# content_type = tableName
# content_type = ContentType.objects.get_for_model(Product)

# getting the Tags of That Item.
# TaggedItem.objects.select_related("tag").filter(
#     content_type=content_type, object_id=1
# )

# -------------
# Custom Manager
# How to Make your Own Manage Functions

# ---
# with transaction.atomic():
#     # ...actions
