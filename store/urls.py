from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from . import views

# router = SimpleRouter()
router = routers.DefaultRouter()
router.register(
    "products",
    views.ProductViewSet,
)
router.register("carts", views.CartViewSet)
router.register("customer", views.CustomerViewSet)

# lookup => product_pk
# basename="product-reviews" => "product-reviews-list", "product-reviews-details"

# LEVEL 1 Nested Routes

## Products/
products_routers = routers.NestedDefaultRouter(router, "products", lookup="product")
products_routers.register("reviews", views.ReviewViewSet, basename="product-reviews")

## Cart/
cart_routers = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_routers.register("items", views.CartItemViewSet, basename="cart-items")

# URLConf
urlpatterns = [
    # Products
    path("", include(router.urls)),
    path("", include(products_routers.urls)),
    path("", include(cart_routers.urls)),
    # collections
    path("collections/", views.CollectionList.as_view()),
    path("collections/<int:pk>/", views.CollectionDetail.as_view()),
]
