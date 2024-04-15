from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from authorization.models import User


class UserLoginForm(AuthenticationForm):
    ...


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Username", max_length=50, required=True)
    email = forms.EmailField(label="E-mail", required=True)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(self.cleaned_data["username"], self.cleaned_data["email"])
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
