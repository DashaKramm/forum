from django.contrib.auth import get_user_model
from django.db import models
from webapp.models import BaseModel


class Reply(BaseModel):
    topic = models.ForeignKey('webapp.Topic', related_name='replies', on_delete=models.CASCADE, verbose_name='Тема')
    content = models.TextField(verbose_name="Содержимое")
    author = models.ForeignKey(
        get_user_model(),
        related_name='replies',
        on_delete=models.SET_DEFAULT,
        default=1
    )

    def __str__(self):
        return f"Ответ на тему {self.topic.title}"

    class Meta:
        db_table = 'replies'
        verbose_name = 'Ответ в теме'
        verbose_name_plural = 'Ответы в теме'
