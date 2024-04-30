from django.urls import path
from . import views

urlpatterns = [
    path("sign-up/", views.UserSignupView.as_view(),name='sign-up'),
    path("sign-in/", views.UserLoginView.as_view(),name='sign-in'),
    path("products/", views.ProductView.as_view(),name='products'),
    path("products/<int:pk>", views.ProductDetailView.as_view()),
    path('add-to-fvrt/<int:food_id>',views.AddFvrtFood.as_view()),
    path('get-fvrt/',views.GetFvrtFood.as_view(),name='add-fvrt-food'),
    path('get-offers/',views.GetSpecialOffer.as_view()),
]
