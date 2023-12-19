from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True )



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    friend_requests_sent = models.ManyToManyField(
        User, symmetrical=False, related_name='sent_friend_requests', blank=True)
    friend_requests_received = models.ManyToManyField(
        User, symmetrical=False, related_name='received_friend_requests', blank=True)

    def __str__(self):
        return self.user.username
    
class UserRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.ForeignKey(User,on_delete=models.CASCADE,related_name='requests')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + "friend requests"


