from django.db import models
from django.urls import reverse

# Create your models here.

from django.contrib.auth.models import ( 
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from phone_field import PhoneField
from .validators.validators import validate_age

class UserManager(BaseUserManager):
    def _create_user(self,email,password,is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Имя пользователя должно быть email адрессом. ')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,password,**extra_fields):
        return self._create_user(email, password, **extra_fields)
    def create_superuser(self,email,password,**extra_fields):
        user = self._create_user(email,password,True,True,**extra_fields)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True, max_length = 200)  
    name = models.CharField(max_length=254, null=True,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)  
    is_staff = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True)  
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True,blank=True)
    birth_date = models.DateField('Date of brth', validators=[validate_age], default=timezone.now().date())
    avatar = models.ImageField('Avatar', upload_to='avatars/', null=True,blank=True)
    phone_number = PhoneField('Telephone Number', blank=True)
    phone_confirmed = models.PositiveIntegerField('Потверждено', default=0000)



    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []  
    EMAIL_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    objects = UserManager()

    def get_absolute_url(self):
        return reverse("users_detail", kwargs={"pk": self.pk})


