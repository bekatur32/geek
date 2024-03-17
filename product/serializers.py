from rest_framework import serializers
from .models import Product, SearchHistory


class ProductSerializer(serializers.ModelSerializer):
    location = serializers.CharField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    likes = serializers.IntegerField(read_only=True)
    discount = serializers.IntegerField(required=False)

    def apply_discount_to_price(self, price, discount):
        if discount > 0 and discount <= 100:
            discounted_price = price - (price * discount) // 100
            return discounted_price
        else:
            return price

    def create(self, validated_data):
        discount = validated_data.get("discount")
        price = validated_data["price"]
        if discount is not None:
            discounted_price = self.apply_discount_to_price(price, discount)
            validated_data["price"] = discounted_price
        return super().create(validated_data)

    class Meta:
        model = Product
        fields = (
            "id",
            "user",
            "name",
            "slug",
            "image",
            "description",
            "price",
            "location",
            "rating",
            "available",
            "created",
            "updated",
            "likes",
            "discount",
        )
        read_only_fields = ("id", "slug", "created", "updated")


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = '__all__'