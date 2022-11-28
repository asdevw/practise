from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
# Create your views here.
from .models import User
from .form import UserForm
class UserView(ListView):
    template_name = 'users/users.html'
    model = User



class UserUpdate(UpdateView):
    from_class = UserForm
    model = User
    template_name = 'users/view.html'
    context_object_name = 'use'
    fields = '__all__'
    success_url = '/'

class ArticleDetailView(DetailView):
    model = User
    template_name = 'users/detail.html'
    context_object_name = 'article-detail'
