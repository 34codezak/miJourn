from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PasswordResetForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'

    class Meta:
        model = User
        fields = ['email']