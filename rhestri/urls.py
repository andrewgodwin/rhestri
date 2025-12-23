from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

import core.views

urlpatterns = [
    path("", core.views.Home.as_view()),
    # Auth
    path("auth/login/", auth_views.LoginView.as_view(template_name="auth/login.html")),
    # Admin
    path("admin/", admin.site.urls),
]
