from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import (post_delete, post_save, pre_delete, pre_save)
from django.template.defaultfilters import slugify
from transliterator import transliterator
from django.core.mail import send_mail, send_mass_mail
from .email import email_template
from django.core.cache import cache
from django.utils import timezone


# Create your models here.


class Bb(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True)
    pub_date = models.DateTimeField('Дата заполнения', default=timezone.now, blank=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'BB'
        verbose_name_plural = 'BBs'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("bb", kwargs={"pk": self.pk})

    def get_absolute_url_del(self):
        return reverse('mainapp:delete_post', kwargs={'pk': self.pk})


@receiver(pre_save, sender=Bb)
def book_pre_created_or_saved(sender, instance, **kwargs):
    print(instance.name)
    instance.slug = slugify(instance.name)



@receiver(post_save, sender=Bb)
def book_created_or_saved(sender, instance, created, **kwargs):
    if created:
        instance.save()




@receiver(post_delete, sender=Bb)
def book_deleted(sender, instance, **kwargs):
    print(email_template.deleted_book['subject'].format(name=instance.name))
    send_mail(
        subject=email_template.deleted_book['subject'].format(name=instance.name),
        message=email_template.deleted_book['message'],
        from_email=email_template.from_email,
        recipient_list=email_template.recipient_list,
        fail_silently=False,
        html_message=email_template.new_book['html_message'],
    )
    cache.set('Book deleted::%(id)d' % {'id': instance.id}, instance)
@receiver(post_save, sender=Bb)
def book_created_or_saved(sender, instance, created, **kwargs):
    if created:
        print(email_template.new_book['subject'])
        send_mail(
            subject=email_template.new_book['subject'],
            message=email_template.new_book['message'],
            from_email=email_template.from_email,
            recipient_list=email_template.recipient_list,
            fail_silently=False,
            html_message=email_template.new_book['html_message'],
        )
        instance.save()
    else:
        message1 = (
            email_template.saved_book['subject'],
            email_template.saved_book['html_message'].format(name=instance.name),
            email_template.from_email,
            email_template.recipient_list,
        )
        message2 = (
            email_template.testing_message['subject'],
            email_template.testing_message['html_message'].format(name=instance.name),
            email_template.from_email,
            email_template.recipient_list.append(email_template.testing_email),
        )
        send_mass_mail((message1,message2),fail_silently=False)
    cache.set('Book saved or created::%(id)d' % {'id': instance.id}, instance)

@receiver(pre_delete,sender=Bb)
def pre_delete_page_unpublish(sender, instance, **kwargs):
    if instance.live:
        instance.unpublish(commit=False)

    for book in Bb.objects.all():
        if book.pk != instance.pk:
            print(book.name)


def register_signal_handlers():
    pre_delete.connect(pre_delete_page_unpublish, sender=Bb)





# from django.db import models  
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin  
# from django.utils import timezone  
# from django.utils.translation import gettext_lazy as _  
# from .managers import CustomUserManager  
# # Create your models here.  
  
# class CustomUser(AbstractBaseUser, PermissionsMixin):  
#     username = None  
#     email = models.EmailField(_('email_address'), unique=True, max_length = 200)  
#     date_joined = models.DateTimeField(default=timezone.now)  
#     is_staff = models.BooleanField(default=False)  
#     is_active = models.BooleanField(default=True)  
      
  
  
#     USERNAME_FIELD = 'email'  
#     REQUIRED_FIELDS = []  
  
#     objects = CustomUserManager()  
      
#     def has_perm(self, perm, obj=None):  
#         "Does the user have a specific permission?"  
#         # Simplest possible answer: Yes, always  
#         return True  
  
#    def is_staff(self):  
#         "Is the user a member of staff?"  
#         return self.staff  
  
#     @property  
#     def is_admin(self):  
#         "Is the user a admin member?"  
#         return self.admin  
  
#     def __str__(self):  
#         return self.email 

class Genre(models.Model):
    genre = models.CharField('Nazvaniy janra', max_length=150,default='',null=True)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.genre

    def get_absolute_url(self):
        return reverse("genre", kwargs={"pk": self.pk})