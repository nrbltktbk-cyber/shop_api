
from django.urls import path
from .views import *

urlpatterns = [
    # categories
    path('categories/', CategoryListView.as_view()),
    path('categories/<int:pk>/', CategoryDetailView.as_view()),

    # products
    path('products/', ProductListView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),

    # reviews
    path('reviews/', ReviewListView.as_view()),
    path('reviews/<int:pk>/', ReviewDetailView.as_view()),
]