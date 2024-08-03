from django.urls import path
from django.views.generic import RedirectView

from webapp.views import TopicListView, CreateTopicView, TopicDetailView, ReplyCreateView, ReplyUpdateView, \
    ReplyDeleteView, TopicUpdateView, TopicDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='webapp:index')),
    path('topics/', TopicListView.as_view(), name='index'),
    path('create/', CreateTopicView.as_view(), name='create_topic'),
    path('topic/<int:pk>/', TopicDetailView.as_view(), name='detailed_topic_view'),
    path('topic/<int:pk>/reply/create/', ReplyCreateView.as_view(), name='create_reply'),
    path('reply/<int:pk>/update/', ReplyUpdateView.as_view(), name='update_reply'),
    path('reply/<int:pk>/delete/', ReplyDeleteView.as_view(), name='delete_reply'),
    path('topic/<int:pk>/update/', TopicUpdateView.as_view(), name='update_topic'),
    path('topic/<int:pk>/delete/', TopicDeleteView.as_view(), name='delete_topic'),
]
