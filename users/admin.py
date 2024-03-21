from django.contrib import admin
from .models import Profile, BulletinBoard, ProfileBulletinBoard, LikePost, FollowersCount, Comment

admin.site.site_header = "Chikaness"
admin.site.site_title = "Chikaness"
admin.site.index_title = "Manage Chikaness"

admin.site.register(Profile)
admin.site.register(BulletinBoard)
admin.site.register(ProfileBulletinBoard)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(Comment)
