from rest_framework import generics
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer


# ===== CATEGORY =====

class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


# ===== PRODUCT =====

class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


# ===== REVIEW =====

class ReviewListAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'


# ===== PRODUCT REVIEWS (ДЗ 2) =====

class ProductReviewsAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = []

        for product in products:
            reviews = product.reviews.all()
            total = sum([r.stars for r in reviews])
            rating = total / len(reviews) if reviews else 0

            data.append({
                "id": product.id,
                "title": product.title,
                "reviews": ReviewSerializer(reviews, many=True).data,
                "rating": round(rating, 2)
            })

        return Response(data)