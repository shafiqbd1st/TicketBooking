"""
URL configuration for TrainTicketBookingSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("activate/<uid64>/<token>/", views.activate, name="activate"),
    path("login/", views.login.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("category/<slug:station_slug>/", views.home, name="category_wise_post"),
    path("deposit/", views.deposit, name="deposit"),
    path("train/", include("Train.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
