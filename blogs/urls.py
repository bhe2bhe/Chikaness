from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('',views.blogs,name="blogs"),
    path('show-blog/<uuid:pk>/',views.show_blog,name="show-blog"),
    path('featured/', views.featured, name="featured"),  
    path('add-comment/',views.add_comment,name="add-comment"),
    path('blog-form/', views.create_blog, name="blog-form"),  # Modified path for blog form
    path('blog-form/<int:blog_id>/', views.create_blog, name='edit-blog'), 
    path('search/', views.search, name="search"),  # Modified path for blog form
    path('delete-blog/<uuid:blog_id>', views.delete_blog, name="delete-blog"),  # Modified path for blog form
    path('delete-confirmation/<uuid:blog_id>', views.delete_confirmation, name="delete-confirmation"),  # Modified path for blog form
    path('categories/<str:category>/', views.category, name="category"),  # Modified path for blog form
    path('<str:username>/', views.user_blogs, name="user-blogs"),  
    
]
