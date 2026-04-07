from django.urls import path
from .views import *

urlpatterns = [
    # categories
    path('categories/', category_list_api_view),
    path('categories/<int:id>/', category_detail_api_view),

    # products
    path('products/', product_list_api_view),
    path('products/<int:id>/', product_detail_api_view),
    path('products/reviews/', product_reviews_api_view),

    # reviews
    path('reviews/', review_list_api_view),
    path('reviews/<int:id>/', review_detail_api_view),
]