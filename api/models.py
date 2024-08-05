from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserProfile(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True,related_name='_followers')
    following = models.ManyToManyField('self', symmetrical=False, blank=True,related_name='_following')
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    groups=None
    user_permissions=None
    

    def count_followers(self):
        return self.followers.count()  
    def count_following(self):
        return self.following.count()
    def count_friend_requests(self):
        return FriendRequests.objects.filter(receiver=self).count()


class FriendRequests(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')