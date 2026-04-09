from rest_framework import serializers
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']

    # кастомная валидация
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Название не может быть пустым")

        if len(value) < 2:
            raise serializers.ValidationError("Минимум 2 символа")

        return value


# ===== PRODUCT =====
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Название обязательно")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше 0")
        return value

    def validate(self, data):
        # общая валидация
        if len(data.get('description', '')) < 5:
            raise serializers.ValidationError({
                "description": "Описание слишком короткое"
            })
        return data

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']

    def validate_text(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Отзыв слишком короткий")
        return value

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Оценка должна быть от 1 до 5")
        return value