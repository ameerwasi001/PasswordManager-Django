from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from ..forms.signup import SignUpForm, Profile, UpdateProfile
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

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