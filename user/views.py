from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm, SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from entries.models import Entry


# Home view
@login_required(login_url='user:login')
class HomeView:
    def get(self, request):
        entries = Entry.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'home.html', {'entries': entries})
    
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

# Logout view   
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import logout

class LogoutView(View):
    def get(self, request):
        return self.process_logout(request)
    
    def post(self, request):
        return self.process_logout(request)
    
    def process_logout(self, request):
        logout(request)
        return redirect('user:login')


class PasswordResetView:
    form_class = UserCreationForm
    template_name = 'password_reset.html'