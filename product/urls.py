from django.urls import path
from . import views

urlpatterns = [
    # Category
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()),

    # Product
    path('products/', views.ProductListAPIView.as_view()),
    path('products/<int:id>/', views.ProductDetailAPIView.as_view()),

    # Review
    path('reviews/', views.ReviewListAPIView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailAPIView.as_view()),

    # Product Reviews
    path('products/reviews/', views.ProductReviewsAPIView.as_view()),
]