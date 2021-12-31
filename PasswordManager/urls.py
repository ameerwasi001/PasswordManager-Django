"""PasswordManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from .views.passwordListing import directory
from .views.auth import signup, edit, create_password
from .views.messages import messages, send_message
from .forms.profile import Profile
from .forms.passwords import Passwords, Message
from django.contrib.auth.decorators import user_passes_test

admin.site.register(Profile)
admin.register(Profile)
admin.site.register(Passwords)
admin.register(Passwords)
admin.site.register(Message)
admin.register(Message)

login_forbidden = user_passes_test(lambda u: u.is_anonymous, '/')
notlogin_forbidden = user_passes_test(lambda u: not u.is_anonymous, '/login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('message/<int:password_id>', notlogin_forbidden(send_message), name="send_message"),
    path('messages', notlogin_forbidden(messages), name="messages"),
    path('', notlogin_forbidden(directory)),
    path('createPassword', notlogin_forbidden(create_password), name="createPassword"),
    path('edit', notlogin_forbidden(edit), name="edit"),
    path('signup', login_forbidden(signup), name="signup"),
    path('login', login_forbidden(LoginView.as_view()), name="login"),
    path('logout', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]
