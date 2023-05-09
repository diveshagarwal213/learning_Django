from decimal import Decimal
from email import message

from rest_framework import serializers

from store.models import Collection, Product


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            "id",
            "title",
        ]


class ProductSerializer(serializers.ModelSerializer):
    # Model Serializer
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "slug",
            "inventory",
            "unit_price",
            "price_with_tax",
            "collection",
        ]
        # fields = '__all__'

    # Custom serializers
    # collection = CollectionSerializer() #
    # price = serializers.DecimalField(
    #     max_digits=6, decimal_places=2, source="unit_price"
    # )
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    # override Methods

    # def validate(self, data):
    #     if True:
    #         return data
    #     else:
    #         return serializers.ValidationError("message")

    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product

    #  User Methods
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
