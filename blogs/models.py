from django.db import models
from users.models import User
import uuid
from datetime import datetime

class Blog(models.Model):
    CATEGORIES = [
        ('education', 'Education'),
        ('music', 'Music'),
        ('personal', 'Personal'),
        ('promotions', 'Promotions'),
        ('travels', 'Travels'),
        ('others', 'Others')
    ]
    
    DEFAULT_CATEGORY = 'others' 
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)    
    featured = models.BooleanField(default=False)
    pen_name = models.CharField(max_length=100, null=True, blank=True)
    teaser = models.TextField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORIES, default=DEFAULT_CATEGORY)
    content = models.TextField()
    content2 = models.TextField(null=True, blank=True)
    content3 = models.TextField(null=True, blank=True)
    content4 = models.TextField(null=True, blank=True)
    content5 = models.TextField(null=True, blank=True)
    content6 = models.TextField(null=True, blank=True)
    content7 = models.TextField(null=True, blank=True)
    content8 = models.TextField(null=True, blank=True)
    content9 = models.TextField(null=True, blank=True)
    content10 = models.TextField(null=True, blank=True)
    image = models.ImageField(default='read-me.jpg', upload_to='blog_pics')
    image_end = models.ImageField(null=True, blank=True, upload_to='blog_pics')    
    image2 = models.ImageField(null=True, blank=True, upload_to='blog_pics')
    image3 = models.ImageField(null=True, blank=True, upload_to='blog_pics')
    image4 = models.ImageField(null=True, blank=True, upload_to='blog_pics')
    image5 = models.ImageField(null=True, blank=True, upload_to='blog_pics')
    image6 = models.ImageField(null=True, blank=True, upload_to='blog_pics')
    image7 = models.ImageField(null=True, blank=True, upload_to='blog_pics')
    image8 = models.ImageField(null=True, blank=True, upload_to='blog_pics')
    image9 = models.ImageField(null=True, blank=True, upload_to='blog_pics')
    image_end_caption = models.CharField(max_length=255, null=True, blank=True)
    image2_caption = models.CharField(max_length=255, default="Photo has no caption")
    image3_caption = models.CharField(max_length=255, default="Photo has no caption")
    image4_caption = models.CharField(max_length=255, default="Photo has no caption")
    image5_caption = models.CharField(max_length=255, default="Photo has no caption")
    image6_caption = models.CharField(max_length=255, default="Photo has no caption")
    image7_caption = models.CharField(max_length=255, default="Photo has no caption")
    image8_caption = models.CharField(max_length=255, default="Photo has no caption")
    image9_caption = models.CharField(max_length=255, default="Photo has no caption")
    
    created_at = models.DateTimeField(default=datetime.now)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.author} -- {self.title}"
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = created_at = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return f"Comment by {self.user.username} on blog {self.blog.title}"
    