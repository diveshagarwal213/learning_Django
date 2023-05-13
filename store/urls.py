from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from . import views

# router = SimpleRouter()
router = routers.DefaultRouter()
router.register("products", views.ProductViewSet)

# review Nested Routes
products_routers = routers.NestedDefaultRouter(
    router, "products", lookup="product"
)  # lookup => product_pk
products_routers.register("reviews", views.ReviewViewSet, basename="product-reviews")
# basename="product-reviews" => "product-reviews-list", "product-reviews-details"

# URLConf
urlpatterns = [
    # Products
    path("", include(router.urls)),
    path("", include(products_routers.urls)),
    # collections
    path("collections/", views.CollectionList.as_view()),
    path("collections/<int:pk>/", views.CollectionDetail.as_view()),
]
