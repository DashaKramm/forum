from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect
from webapp.models import Topic, Reply
from webapp.forms import ReplyForm


class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'topics/topic_detail.html'

    def get_success_url(self):
        return reverse_lazy('webapp:detailed_topic_view', kwargs={'pk': self.kwargs['pk']})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'topic': self.kwargs['pk']}
        return kwargs

    def form_valid(self, form):
        form.instance.topic = get_object_or_404(Topic, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = get_object_or_404(Topic, pk=self.kwargs['pk'])
        context['replies'] = context['topic'].replies.all().order_by('created_at')
        return context


class ReplyUpdateView(PermissionRequiredMixin, UpdateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'replies/update_reply.html'
    permission_required = 'webapp.change_reply'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse_lazy('webapp:detailed_topic_view', kwargs={'pk': self.object.topic.pk})


class ReplyDeleteView(PermissionRequiredMixin, DeleteView):
    model = Reply
    template_name = 'replies/delete_reply.html'
    permission_required = 'webapp.delete_reply'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('webapp:detailed_topic_view', kwargs={'pk': self.object.topic.pk})

    def delete(self, request, *args, **kwargs):
        if not request.POST.get('confirm_delete'):
            return redirect('webapp:detailed_topic_view', pk=self.object.topic.pk)
        return super().delete(request, *args, **kwargs)
