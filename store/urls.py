from django.urls import path

from . import views

# URLConf
urlpatterns = [
    # Products
    path("products/", views.product_list),
    path("products/<int:id>/", views.product_detail),
    # Collection
    path("collections/", views.collection_list),
    path("collections/<int:pk>/", views.collection_detail),
]
