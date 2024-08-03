from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', verbose_name='Аватар')

    def __str__(self):
        return self.username

    class Meta:
        db_table = "custom_users"
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
