from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Product


class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choisissez un pseudo...'}),
            'email': forms.TextInput(attrs={'placeholder': 'Adresse mail...'}),
        }


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['new_username', 'new_email']

    new_username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nouveau pseudo'}))
    new_email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nouvelle adresse mail'}))

    @staticmethod
    def update_user(actual_user_data, new_username, new_email, password, commit=True):

        new_user_data = User.objects.create(
            username=new_username,
            email=new_email,
            password=password  # Password no change
        )
        actual_user_data.delete()
        if commit:
            new_user_data.save()
        return new_user_data


class ChangePasswordForm(SetPasswordForm):

    class Meta:
        model = User
        fields = ['new_password1', "new_password2"]

    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nouveau mot de passe'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer le nouveau mot de passe'}))
