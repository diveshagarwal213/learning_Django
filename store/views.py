from django.db.models import Count, F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from store.filters import ProductFilter
from store.models import Collection, OrderItem, Product, Review
from store.pagination import DefaultPagination
from store.serializers import CollectionSerializer, ProductSerializer, ReviewSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # generic-Filter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # search Filters
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]

    # django_filters
    filterset_class = ProductFilter
    # filterset_fields = ["collection_id"]

    # Pagination
    pagination_class = DefaultPagination

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionList(ListCreateAPIView):
    def get_queryset(self):
        query_set = Collection.objects.annotate(products_count=Count("products")).all()
        return query_set

    def get_serializer_class(self):
        return CollectionSerializer


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


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}
