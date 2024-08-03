from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

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
    paginate_by = 2

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


class TopicUpdateView(PermissionRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'topics/update_topic.html'
    permission_required = 'webapp.change_topic'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse_lazy('webapp:detailed_topic_view', kwargs={'pk': self.object.topic.pk})


class TopicDeleteView(PermissionRequiredMixin, DeleteView):
    model = Topic
    template_name = 'topics/delete_topic.html'
    permission_required = 'webapp.delete_topic'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('webapp:index')

    def delete(self, request, *args, **kwargs):
        if not request.POST.get('confirm_delete'):
            return redirect('webapp:detailed_topic_view', pk=self.object.topic.pk)
        return super().delete(request, *args, **kwargs)
