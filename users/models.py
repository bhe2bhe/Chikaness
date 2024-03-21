from django.contrib.auth.models import User
from django.db import models
import uuid
from datetime import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    motto = models.TextField(max_length=300, default="Best friends don’t let you do stupid things alone.")
    about_yourself = models.TextField(max_length=2000, default="😀")
    profile_pic = models.ImageField(default='profilepic.jpg',upload_to='profile_pictures')
    q1 = models.TextField(max_length=1000, default="No answer yet.")
    q2 = models.TextField(max_length=1000, default="No answer yet.")
    q3 = models.TextField(max_length=1000, default="No answer yet.")
    q4 = models.TextField(max_length=1000, default="No answer yet.")
    verified = models.BooleanField(default=False)

    # create imagefield here
    
    def __str__(self):
        return self.user.username


class BulletinBoard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(default='read-me.jpg', upload_to='announcement_pics')
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    no_of_comments = models.IntegerField(default=0)
    highlight = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user} -- {self.content}"
    
class ProfileBulletinBoard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4) 
    user = models.CharField(max_length=100)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return f"Post by {self.user} - on {self.profile}'s profile"
    
class LikePost(models.Model):
    post = models.ForeignKey(BulletinBoard, on_delete=models.CASCADE, related_name='likes', default=None)
    username = models.CharField(max_length=500)
    
    def __str__(self):
        return f"{self.username} liked {self.post_id}"
    
class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.follower} started following {self.user}'
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('BulletinBoard', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    
    class Meta:
        ordering = ['-created_at']  # Order by 'created_at' field in descending order
    
    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post.id}"
    