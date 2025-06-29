from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import LoginForm, SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy



# Home view
@login_required(login_url='user:login')
class HomeView:
    def get(self, request):
        return render(request, 'home.html')
    
# Login view
class LoginView:
    def get(self, request):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('home')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
# Signup view
class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('entries:home')
    
class LogoutView:
    success_url = reverse_lazy('entries:home')

class PasswordResetView:
    template_name = 'password_reset.html'