from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'pen_name', 'teaser', 'content', 'image', 'image_end', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8', 'image9', 'category']
