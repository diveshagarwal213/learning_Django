import random

from django.shortcuts import render
from rest_framework import serializers
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import VerifyPhoneNumber
from .serializers import VerifyPhoneNumberSerializer

# Create your views here.


# class VerifyPhoneNumberApiView(APIView):
#     def post(self, request):
#         serializer = VerifyPhoneNumberSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # serializer.save()


#         return Response(request.data)
class VerifyPhoneNumberApiViewSet(ModelViewSet):
    http_method_names = ["post"]

    queryset = VerifyPhoneNumber.objects.all()
    serializer_class = VerifyPhoneNumberSerializer
