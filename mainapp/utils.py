from .models import Genre


menu = [{'title':'Главная','home':'mainapp:home'},
{'title':'Добавить книгу:','create':'mainapp:create'},
{'title':'Посмотреть жанры','genre':'mainapp:genre'},
]

class DataMixin:
    def get_user_context(self,**kwargs):
        user_menu = menu.copy()
        context=kwargs
        genre = Genre.objects.all()
        context['menu'] = user_menu
        context['genre'] = genre

        return context