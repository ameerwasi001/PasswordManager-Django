from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, authenticate
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from ..forms.profile import SignUpForm, Profile, UpdateProfile
from ..forms.passwords import Passwords, PasswordForm
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..encryption import generate_rsa_keys

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            instance = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            profile = Profile.objects.create(user=instance)
            pub_key, enc_priv_key = generate_rsa_keys(raw_password)
            profile.public_key = pub_key
            profile.encrypted_private_key = enc_priv_key
            profile.save()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('signup')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def create_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        password = request.user.password
        password_entered = request.POST.get("given_user_password")
        form.user = request.user
        if form.is_valid() and check_password(password_entered, password):
            form.save(password_entered)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'passwords/passwordform.html', {"form": form})
    form = PasswordForm()
    return render(request, 'passwords/passwordform.html', {"form": form})

def edit(request):
    profile = Profile.objects.get(user_id = request.user)
    args = {}

    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        form.user = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = UpdateProfile(initial={"name": profile.name})

    args['form'] = form
    return render(request, 'registration/edit.html', args)