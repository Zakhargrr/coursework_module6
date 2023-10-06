from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView

from users.forms import UserRegisterForm, UserProfileForm, UserLoginForm
from users.models import User
import secrets


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()
        new_user.generated_key = secrets.token_urlsafe(16)
        new_user.user_key = None
        new_user.save()
        send_mail(
            subject="Ключ для верификации почты",
            message=f"{new_user.generated_key} - ваш ключ для верификации почты",
            from_email="noreply@oscarbot.ru",
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        edit_user = form.save()
        if edit_user.user_key == edit_user.generated_key:
            edit_user.is_verified = True
        else:
            edit_user.user_key = None
        return super().form_valid(form)


class CustomLoginView(LoginView):
    form_class = UserLoginForm


class UserListView(ListView):
    model = User

    def get_queryset(self):
        if not self.request.user.is_staff:
            raise Http404
        return super().get_queryset()


def ban_user(request, pk):
    if not request.user.is_staff:
        raise Http404
    user = User.objects.get(pk=pk)
    if not user.is_active:
        user.is_active = True
    else:
        user.is_active = False
    user.save()
    return redirect(reverse('users:creators'))

