from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    #"self" string as the first argument in the ManyToManyField to indicate a self-referencing relationship
    followers = models.ManyToManyField("self",blank=True,related_name="followersuserprofile",symmetrical=False)
    following = models.ManyToManyField("self",blank=True,related_name="followinguserprofile",symmetrical=False)


class Posts(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Post")
    content = models.CharField(max_length=300)
    likecount = models.IntegerField(default=0)
    users_who_liked = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    submissiontime = models.DateTimeField()

    def is_liked_by_user(self, user):
        try:
            Like.objects.get(user=user, post=self)
            return True
        except Like.DoesNotExist:
            return False

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

