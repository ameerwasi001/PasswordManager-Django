from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponseRedirect
from PasswordManager.encryption import whole_decrypt
from PasswordManager.forms.passwords import Passwords

def directory(request):
    errors = False
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    if request.method == "POST":
        password_entered = request.POST.get("given_user_password")
        password = request.user.password
        if check_password(password_entered, password):
            passwords = Passwords.objects.filter(user_id=request.user)
            for password in passwords:
                password.password = whole_decrypt(password.encrypted_password, password.encrypted_key, password_entered)
            return render(request, 'passwordListing.html', {"passwords": passwords, "show_password": True})
        else:
            errors = True
    passwords = Passwords.objects.filter(user_id=request.user)
    for password in passwords:
        password.password = "****"
    return render(request, 'passwordListing.html', {"passwords": passwords, "show_password": False, "errors": errors})
