from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.views import LoginView as BaseLoginView

from accounts.forms import CustomUserCreationForm
from webapp.models import Topic, Reply

# Create your views here.
User = get_user_model()


class LoginView(BaseLoginView):
    template_name = "login.html"

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.context_data['has_error'] = True
        return response


class RegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration.html"
    model = User

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:index')
        return next_url


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['replies_count'] = Reply.objects.filter(author=user).count()
        user_topics = Topic.objects.filter(author=user).annotate(replies_count=Count('replies')).order_by('-created_at')
        page = self.request.GET.get('page', 1)
        paginator = Paginator(user_topics, 3)
        topics_page = paginator.get_page(page)
        context['user_topics'] = topics_page
        context['is_paginated'] = paginator.num_pages > 1
        context['paginator'] = paginator
        context['page_obj'] = topics_page
        return context
