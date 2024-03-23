from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'pen_name', 'teaser', 'content', 'content2', 'content3', 'content4', 'content5', 'content6', 'content7', 'content8', 'content9', 'content10', 'category', 'image', 'image_end', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8', 'image9', 'image_end_caption', 'image2_caption', 'image3_caption', 'image4_caption', 'image5_caption', 'image6_caption', 'image7_caption', 'image8_caption', 'image9_caption']
