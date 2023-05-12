# Class Based Views 

## Create & List 

#### APIView
```python
class ProductList(APIView):
def get(self, req):
    query_set = Product.objects.select_related("collection").all()
    serializer = ProductSerializer(query_set, many=True)
    return Response(serializer.data)

def post(self, req):
    serializer = ProductSerializer(data=req.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
```
#### ListCreateApiView
```python
class ProductList(ListCreateAPIView):
    # queryset=
    # serializer_class=

    def get_queryset(self):
        query_set = Product.objects.all()
        return query_set

    def get_serializer_class(self):
        return ProductSerializer

    # def get_serializer_context(self):
    #     return {'request':self.request}
```

## get, Update & Delete

#### RetrieveUpdateDestroyAPIView

```python
class ProductDetail(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_class(self):
        return ProductSerializer
```

### Function based
```python
@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        if product.orderitem_set.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```