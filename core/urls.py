from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register(
    "phone_number",
    views.VerifyPhoneNumberApiViewSet,
)

urlpatterns = [
    # Products
    path("", include(router.urls)),
]
