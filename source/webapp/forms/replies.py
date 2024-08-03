from django import forms
from django.forms import widgets

from webapp.models import Reply


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': widgets.Textarea(attrs={"cols": 127, "rows": 5}),
        }
