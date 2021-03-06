from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, HttpResponseRedirect
from PasswordManager.encryption import password_encrypt, whole_decrypt, password_decrypt, rsa_encrypt, rsa_decrypt
from PasswordManager.forms.passwords import Message, Passwords, SendPasswordForm
from django.contrib.auth.models import User

def send_message(request, password_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    website_password = Passwords.objects.get(id = password_id)
    user = request.user
    if website_password.user_id != user.id:
        return HttpResponseForbidden()
    if request.method == 'POST':
        password_entered = request.POST.get("given_user_password")
        password = user.password
        enc_key = website_password.encrypted_key
        form = SendPasswordForm(request.POST)
        found = True
        try:
            other_user = User.objects.get(username = request.POST.get("receiver"))
        except:
            found = False
        pass_check = check_password(password_entered, password)
        if form.is_valid() and pass_check and found:
            dec_key = password_decrypt(enc_key.encode(), password_entered).decode()
            dec_rsa_key = rsa_encrypt(other_user.profile.public_key, dec_key)
            form.save(website_password, user, dec_rsa_key, other_user)
            return HttpResponseRedirect("/")
        else:
            return render(
                request, 
                'passwords/sendPassword.html', {
                    "form": form, 
                    "no_user_found": not found,
                    "incorrect_password": not pass_check
                }
            )
    form = SendPasswordForm()
    return render(request, 'passwords/sendPassword.html', {"form": form})

def messages(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    user = request.user
    messages = Message.objects.filter(receiver_id = user)
    if request.method == "POST":
        password_entered = request.POST.get("given_user_password")
        password = user.password
        if not check_password(password_entered, password):
            for message in messages:
                message.password.password = "****"
            return render(
                request, 
                "passwords/messageListing.html", 
                {"messages": messages, "show_password": False, "error": True}
            )
        for message in messages:
            enc_key = message.encrypted_key
            if enc_key == "" or enc_key == None:
                enc_priv_key = user.profile.encrypted_private_key
                dec_key = rsa_decrypt(enc_priv_key, password_entered, message.decrypted_key)
                message.encrypted_key = password_encrypt(dec_key.encode(), password_entered).decode()
                enc_key = message.encrypted_key
                message.decrypted_key = ""
                message.save()
            message.password.password = whole_decrypt(message.password.encrypted_password, enc_key, password_entered)
        return render(request, "passwords/messageListing.html", {"messages": messages, "show_password": True})
    for message in messages:
        message.password.password = "****"
    return render(request, "passwords/messageListing.html", {"messages": messages, "show_password": False})
