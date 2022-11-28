from django.contrib import admin
from .models import *
# Register your models here.

# @admin.site(Bb)
class AdminBb(admin.ModelAdmin):
    search_fields = ('name',)
    list_editable =('slug', 'is_published')
    list_display = ['name', 'slug', 'is_published']
    list_display_links = ('name',)
    list_filter = ('is_published','name','slug',)

    def get_list_display(self,request):
        l_d = ['name','slug','is_published']
        if(request.user.is_superuser):
            l_d+=['is_published']
        return l_d

    def get_search_fields(self,request):
        if(request.user.is_superuser):
            s_f = ['name','slug']
            return s_f
        else:
            s_f = ['name']
            return s_f
    def get_list_filter(self,request):
        if(request.user.is_superuser):
            s_f = ['name','slug','is_published']
            return s_f
        else:
            s_f = ['is_published']
            return s_f

admin.site.register(Bb, AdminBb)