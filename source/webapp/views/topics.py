from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from webapp.forms.topics import TopicForm
from webapp.models import Topic


# Create your views here.
class TopicListView(ListView):
    model = Topic
    template_name = 'topics/topics_list.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return Topic.objects.annotate(replies_count=Count('replies')).order_by('-created_at')


class CreateTopicView(LoginRequiredMixin, CreateView):
    template_name = "topics/create_topic.html"
    form_class = TopicForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('webapp:index')
