from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("products", views.ProductViewSet)

# URLConf
urlpatterns = [
    # Products
    path("", include(router.urls)),
    # collections
    path("collections/", views.CollectionList.as_view()),
    path("collections/<int:pk>/", views.CollectionDetail.as_view()),
]
