from rest_framework import generics
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def products_with_reviews(request):
    products = Product.objects.all()
    data = []

    for product in products:
        reviews = product.reviews.all()
        reviews_data = []
        total = 0

        for review in reviews:
            reviews_data.append({
                'text': review.text,
                'stars': review.stars
            })
            total += review.stars

        avg_rating = total / len(reviews) if reviews else 0

        data.append({
            "id": product.id,
            "title": product.title,
            "reviews": reviews_data,
            "rating": round(avg_rating, 2)
        })

    return Response(data)


@api_view(['GET'])
def categories_with_count(request):
    categories = Category.objects.all()
    data = []

    for category in categories:
        count = category.product_set.count()
        data.append({
            "id": category.id,
            "name": category.name,
            "products_count": count
        })

    return Response(data)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer