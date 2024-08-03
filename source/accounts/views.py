from django.contrib.auth import get_user_model, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as BaseLoginView

from accounts.forms import CustomUserCreationForm

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
