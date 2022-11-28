from django.urls import path
from .views import *
from config.settings import CACHE_TTL
from django.views.decorators.cache import cache_page
app_name = 'mainapp'
urlpatterns = [
    path('', cache_page(settings.CACHE_TTL)(IndexView.as_view()), name='home'),
    path('create/', CreateView.as_view(), name='create'),
    path('success/', Suc.as_view(), name='success'),
    path('change/<int:pk>', Updater.as_view(), name='change'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
    path('article/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('sendermail/', sendMail, name='sender'),
    path('genre/',GenreBooks.as_view(), name='genre'),

]