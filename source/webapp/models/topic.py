from django.contrib.auth import get_user_model
from django.db import models
from webapp.models import BaseModel


class Topic(BaseModel):
    title = models.CharField(max_length=100, verbose_name="Название")
    content = models.TextField(verbose_name="Содержимое")
    author = models.ForeignKey(
        get_user_model(),
        related_name='topics',
        on_delete=models.SET_DEFAULT,
        default=1
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'topics'
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
