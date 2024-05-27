from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import View


from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User

from TrainStation.models import Station
from Train.models import Train, UserProfile


def home(request, station_slug=None):
    train = Train.objects.all()

    if station_slug is not None:
        station = Station.objects.get(slug=station_slug)
        train = Train.objects.filter(station=station)

    station = Station.objects.all()
    return render(request, "home.html", {"train": train, "station": station})


def register(request):
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your account"
            message = render_to_string(
                "registerEmail.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            send_mail = form.cleaned_data.get("email")

            email = EmailMultiAlternatives(mail_subject, "", to=[send_mail])
            email.attach_alternative(message, "text/html")
            email.send()
            messages.success(request, "User registration Successfully")
            messages.info(request, "Activate your account from the mail you provided")
            return redirect("home")
    else:
        form = forms.RegisterForm()
    return render(request, "register.html", {"form": form})


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is activated now, you can now login")
        return redirect("login")
    else:
        messages.warning(request, "activation link is invalid")
        return redirect("register")


class login(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        messages.success(self.request, "Login Successfully")
        return reverse_lazy("home")


class UserLogoutView(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            logout(request)
            messages.info(self.request, f"Logout successfully!")
        return redirect("home")


@login_required
def deposit(request):
    if request.method == "POST":
        user = UserProfile.objects.get(user=request.user)
        print(request.user)
        form = forms.depositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            user.balance += amount
            user.save()
            messages.success(request, "Deposit Successfully Added")
            # send_transaction_email(
            #     request.user,
            #     amount,
            #     "Deposit Message",
            #     "deposit_email.html",
            # )
            return redirect("home")
    else:
        form = forms.depositForm()
    return render(request, "deposit.html", {"form": form})
