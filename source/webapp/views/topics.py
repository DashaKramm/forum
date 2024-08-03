from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from webapp.forms import TopicForm, ReplyForm
from webapp.models import Topic


# Create your views here.
class TopicListView(ListView):
    model = Topic
    template_name = 'topics/topics_list.html'
    context_object_name = 'topics'
    paginate_by = 3

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


class TopicDetailView(DetailView):
    model = Topic
    template_name = 'topics/topic_detail.html'
    context_object_name = 'topic'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        replies = self.object.replies.annotate(message_count=Count('author__replies')).order_by('created_at')
        paginator = Paginator(replies, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['replies'] = page_obj.object_list
        context['is_paginated'] = page_obj.has_other_pages()
        context['reply_form'] = ReplyForm()
        return context
