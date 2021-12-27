from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ..encryption import whole_encrypt, whole_decrypt

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user)

class Passwords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    websitename = models.CharField(max_length=255, null=True)
    websiteusername = models.CharField(max_length=255, null=True)
    encrypted_password = models.TextField()
    encrypted_key = models.TextField()
    url = models.URLField()

    def __str__(self):
        return "pass: " + str(self.user)

class PasswordForm(ModelForm):
    websitename = forms.CharField(required=True)
    url = forms.URLField(required=True)
    websitepassword = forms.CharField(required=True)
    given_user_password = models.CharField(max_length=255)
    class Meta:
        model = Passwords
        fields = ('websitename', 'websiteusername', 'url', 'websitepassword')

    def save(self, master_password, commit=True):
        instance = super(PasswordForm, self).save(commit=False)
        instance.user = self.user
        website_password = self.cleaned_data['websitepassword']
        enc_key, enc_data = whole_encrypt(website_password, master_password)
        instance.encrypted_password = enc_data
        instance.encrypted_key = enc_key
        if commit:
            instance.save()
        return instance

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
