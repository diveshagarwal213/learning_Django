from django.urls import path

from . import views

# URLConf
urlpatterns = [
    # Products
    path("products/", views.ProductList.as_view()),
    path("products/<int:id>/", views.ProductDetail.as_view()),
    # Collection
    path("collections/", views.CollectionList.as_view()),
    path("collections/<int:pk>/", views.CollectionDetail.as_view()),
]
