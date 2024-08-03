from django.urls import path
from django.views.generic import RedirectView

from webapp.views import TopicListView, CreateTopicView

app_name = 'webapp'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='webapp:index')),
    path('projects/', TopicListView.as_view(), name='index'),
    path('create/', CreateTopicView.as_view(), name='create_topic'),
]
