from django.db.models import Count, F
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from store.models import Collection, Product
from store.serializers import CollectionSerializer, ProductSerializer


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


class ProductDetail(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"

    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_class(self):
        return ProductSerializer

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(["GET", "PUT", "DELETE"])
# def product_detail(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == "GET":
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "DELETE":
#         if product.orderitem_set.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


### COLLECTION
# Create your views here.
class CollectionList(ListCreateAPIView):
    def get_queryset(self):
        query_set = Collection.objects.annotate(products_count=Count("products")).all()
        return query_set

    def get_serializer_class(self):
        return CollectionSerializer


# @api_view(["GET", "PUT"])  # "DELETE"
# def collection_detail(request, pk):
#     collection = get_object_or_404(
#         Collection.objects.annotate(products_count=Count("products")), pk=pk
#     )
#     if request.method == "GET":
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == "PUT":
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == "DELETE":
#         if collection.products.count() > 0:
#             return Response(
#                 {"error": "error_custom_message"},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             )
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Collection.objects.annotate(products_count=Count("products"))

    def get_serializer_class(self):
        return CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response(
                {"error": "error_custom_message"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
