from django.urls import path, include
from .views import *
app_name = 'users'
urlpatterns = [
    path('userview/' ,UserView.as_view(), name = 'userv'),
    path('user/<int:pk>/', UserUpdate.as_view(), name='users'),
    path('detail_view/<int:pk>',ArticleDetailView.as_view(), name='article-detail'),
]