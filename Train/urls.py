from django.urls import path
from . import views


urlpatterns = [
    path("detail/<int:id>", views.Detail.as_view(), name="detail"),
    path("booking/<int:id>/", views.buy_ticket, name="booking"),
    path("profile", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/edit/password_change/", views.pass_change, name="pass_change"),
    
]
