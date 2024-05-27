from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from . import models
from . import forms
from .forms import ChangeUserData
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    SetPasswordForm,
)

@method_decorator(login_required, name="dispatch")
class Detail(DetailView):
    model = models.Train
    pk_url_kwarg = "id"
    template_name = "train_detail.html"
    
        
    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        train = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.train = train
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        train = self.object
        comments = train.comments.all()
        comment_form = forms.CommentForm()

        context["comments"] = comments
        context["comment_form"] = comment_form
        return context


@login_required
def profile(request):
    data = models.BuyTicket.objects.filter(name=request.user)
    return render(request, "profile.html", {"data": data})


# def buy_ticket(request, id):
#     booking = 1
#     train = models.Train.objects.get(id=id)
#     if train.totalTicket >= booking:
#         train.totalTicket -= booking
#         train.save()

#         booking = models.BuyTicket()
#         booking.name = request.user
#         booking.buyTicket = models.Train.objects.get(id=id)

#         new_user = models.UserProfile.objects.get(user=request.user)

#         new_user.balance -= booking.buyTicket.ticketPrice
#         new_user.save()
#         booking.save()

#         messages.success(request, "Ticket this booking Successfully")
#         return redirect("detail", id)
#     else:
#         messages.error(request, "Not Found")
#         return redirect("detail", id)

def buy_ticket(request, id):
    ticket = 1
    train = models.Train.objects.get(id=id)
    booking = models.BuyTicket()
    booking.name = request.user
    booking.buyTicket = models.Train.objects.get(id=id)
    new_user = models.UserProfile.objects.get(user=request.user)
    x = int(new_user.balance)
    y = int(booking.buyTicket.ticketPrice)

    if train.totalTicket >= ticket:
        if x >= y:
            train.totalTicket -= ticket
            train.save()

            new_user.balance -= booking.buyTicket.ticketPrice
            new_user.save()
            booking.save()

            messages.success(request, "Ticket this booking Successfully")
        else:
            messages.warning(request, "Don't have sufficient balance")
        return redirect("detail", id)
    else:
        messages.error(request, "can not purchase the ticket")
        return redirect("detail", id)

# hello
@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ChangeUserData(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Update successfully")
            return redirect("profile")

    else:
        form = ChangeUserData(instance=request.user)
    return render(request, "update_profile.html", {"form": form})


@login_required
def pass_change(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = SetPasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, "Password changed successfully")
                return redirect("profile")
        else:
            form = SetPasswordForm(user=request.user)
        return render(request, "pass_change.html", {"form": form})
    else:
        return redirect("login")
