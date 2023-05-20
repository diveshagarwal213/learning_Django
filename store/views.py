from urllib import request

from django.db.models import Count, F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from store.filters import ProductFilter
from store.models import (
    Cart,
    CartItem,
    Collection,
    Customer,
    OrderItem,
    Product,
    Review,
)
from store.pagination import DefaultPagination
from store.permissions import (
    FullDjangoModelPermissions,
    IsAdminOrReadOnly,
    ViewCustomerHistoryPermission,
)
from store.serializers import (
    AddCartItemSerializer,
    CartItemSerializer,
    CartSerializer,
    CollectionSerializer,
    CustomerSerializers,
    ProductSerializer,
    ReviewSerializer,
    UpdateCartItemSerializer,
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # permission
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        query_set = Collection.objects.annotate(products_count=Count("products")).all()
        return query_set

    def get_serializer_class(self):
        return CollectionSerializer


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]

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


class CartViewSet(
    CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return CartItem.objects.select_related("product").filter(
            cart_id=self.kwargs["cart_pk"]
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        if self.request.method == "PATCH":
            return UpdateCartItemSerializer

        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers

    permission_classes = [IsAdminUser]  # Apply to All Views
    # permission_classes = [FullDjangoModelPermissions]  # Custom permission

    # def get_permissions(self):
    #     if self.request.method == "GET":
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    # Custom End Point
    @action(
        detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated]
    )  # details=False ? will show on details page(customer/1/me) :  will show on List page(customer/me)
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == "GET":
            # request.user # Anonymous || UserInstance
            serializer = CustomerSerializers(customer)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = CustomerSerializers(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response("Ok")
