from django.db import models
from django.contrib.auth.models import User
from TrainStation.models import Station

# Create your models here.

class Train(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    station = models.ManyToManyField(Station)
    ticketPrice = models.IntegerField(default=0)
    totalTicket = models.IntegerField(default=20, null=True, blank=True)
    image = models.ImageField(upload_to="Train/media/", blank=True, null=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user")
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return self.user.username

# class addTicket(models.Model):
#     train = models.ForeignKey(Train, on_delete=models.CASCADE, blank=True, null=True)
#     ticket = models.BooleanField(default=False)


class BuyTicket(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    buyTicket = models.ForeignKey(Train, on_delete=models.CASCADE, blank=True, null=True)
    buyDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name.username


class Comment(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=30)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comments by {self.name}"
