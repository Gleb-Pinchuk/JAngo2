from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('catalog:home')

    def get_success_url(self):
        return self.success_url

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Отправка приветственного письма
            send_mail(
                subject='Добро пожаловать на наш сайт!',
                message=f'Здравствуйте, {user.email}! Спасибо за регистрацию.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            # Автоматический вход после регистрации
            login(request, user)
            return redirect('catalog:home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
