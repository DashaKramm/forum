from django import forms
from django.forms import widgets

from webapp.models import Topic


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']
        widgets = {
            'content': widgets.Textarea(attrs={"cols": 24, "rows": 5}),
        }
