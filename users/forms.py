from django.core.exceptions import ValidationError
from django.forms import EmailField, CharField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from .models import ValidEmail
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import TextInput


class CustomAuthForm(AuthenticationForm):
    username = UsernameField(widget=TextInput(attrs={'autofocus': True}), label='Username or Email')


class SignupForm(UserCreationForm):
    email = EmailField(max_length=254, help_text='Please provide the email address SAC has on file.')
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if not ValidEmail.objects.filter(email=email).exists():
            raise ValidationError(
                'This email is not on file with the Skagit Alpine Club. '
                'If you believe this an error please email skagitalpineclubwebsite@gmail.com.')
        return email

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ProfileForm(UserChangeForm):
    password = None
    email = EmailField(max_length=254)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
