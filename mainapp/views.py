from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import *
from .models import *
from django.views.generic import ListView, TemplateView
from django.core.signing import Signer
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, cache_page
from django.views.decorators.http import condition, etag, last_modified
from config import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .utils import DataMixin

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
def get_last_modified(request, *args, **kwargs):
    return timezone.now()

def get_etag(request, *args, **kwargs):
    etag = '1234455514544'
    return etag
def latest_entry(request, pk):
    pub_date = Bb.objects.filter(pk=pk).first()
    return pub_date.pub_dat


# Create your views here.
class CreateView(SuccessMessageMixin ,CreateView):
    model = Bb
    template_name = 'create.html'
    # context_object_name = ''
    success_url = '/success/'
    form_class = BbForm
    singer = Signer()
    val = singer.sign('Django')
    success_message = 'Мы создали надпись https://github.com/asdevw'



@method_decorator(cache_page(CACHE_TTL), name='dispatch')
@method_decorator(last_modified(get_last_modified), name='dispatch')
@method_decorator(etag(get_etag), name='dispatch')
class IndexView(ListView):
    model = Bb
    template_name = 'index.html'
    paginate_by = 2

    # def get_context_data(self,*,object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Книга")
    #     return dict(list(context.items()+list(c_def.items())))
    # def get_quersyt(self):
    #     return Genre.objects.all()
    # posts = Bb.objects.values_list()
    # some_post = posts[0]
    # print(some_post.name)

class GenreBooks(DataMixin,ListView):
    model = Genre
    template_name = "navbar.html"
    paginate_by = 10
    fields = '__all__'
    context_object_name = 'genres'

    def get_context_data(self,*,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Жанры")
        return dict(list(context.items()+list(c_def.items())))
    def get_quersyt(self):
        return Genre.objects.all()

class Suc(TemplateView):
    template_name = 'success.html'



class Updater(SuccessMessageMixin, UpdateView):
    model = Bb
    # context_object_name = 'change'
    form_class = BbForm
    template_name ='change.html'
    success_url = '/success/'
    success_message = 'Мы создали надпись'



class ArticleDetailView(SuccessMessageMixin, DetailView):
    model = Bb
    template_name = 'personal.html'
    context_object_name = 'change_detail'



class DeletePostView(DeleteView):
    model = Bb
    template_name = 'delete.html'
    success_url ='/'
    context_object_name = 'delete'

    def get_object(self)->Bb:
        pk_ = self.kwargs.get('pk')

        return get_object_or_404(Bb, pk=pk_)



    def get_success_url(self)->str:
        return reverse('mainapp:home')

    def get_success_message(self, cleaned_data):
        return self.success_message%dict(cleaned_data,name=self.object_name)








def sendMail(request):

    # create a variable to keep track of the form
    messageSent = False

    # check if form has been submitted
    if request.method == 'POST':

        form = EmailForm(request.POST)

        # check if data from the form is clean
        if form.is_valid():
            cd = form.cleaned_data
            subject = "Sending an email with Django"
            message = cd['message']

            # send the email to the recipent
            send_mail(subject, message,
                      settings.DEFAULT_FROM_EMAIL, [cd['recipient']])

            # set the variable initially created to True
            messageSent = True

    else:
        form = EmailForm()

    return render(request, 'email.html', {

        'form': form,
        'messageSent': messageSent,

    })