from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    public_key = models.TextField()
    encrypted_private_key = models.TextField()

    def __str__(self):
        return str(self.user)

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('name',)

class UpdateProfile(ModelForm):
    name = forms.CharField(required=True)

    class Meta:
        model = Profile
        fields = ('name',)

    def save(self, commit=True):
        profile = Profile.objects.get(user_id = self.user)
        profile.name = self.cleaned_data['name']
        if commit:
            profile.save()
        return profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
