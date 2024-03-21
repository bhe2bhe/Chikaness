from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Blog, User, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib import messages
from .forms import BlogForm
from django.contrib.auth.decorators import login_required

def blogs(request):
    all_blogs = Blog.objects.all()
    
    # Number of blogs to display per page
    per_page = 18  # You can adjust this as needed
    
    # Paginate blogs
    paginator = Paginator(all_blogs, per_page)
    
    # Get current page number from request, default to 1
    page_number = request.GET.get('page', 1)

    try:
        # Get blogs for the requested page
        blogs_page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        blogs_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results
        blogs_page = paginator.page(paginator.num_pages)
    
    return render(request, 'blogs/index.html', {'blogs':blogs_page})

def show_blog(request, pk):
    # Retrieve the blog post using the primary key (pk)
    blog = get_object_or_404(Blog, id=pk)
    
    comments = Comment.objects.filter(blog=blog)
    
    # Pass the blog object to the template for rendering
    return render(request, 'blogs/blog.html', {'blog': blog, 'comments':comments})

# @login_required
# def create_blog(request):    
#     categories = Blog.CATEGORIES 
#     blog_id = request.GET.get('blog_id')
#     if blog_id:
#         blog = get_object_or_404(Blog, pk=blog_id)
#     else:
#         blog = None
    
#     if request.method == 'POST':
#         form = BlogForm(request.POST, request.FILES, instance=blog)
#         if form.is_valid():
#             # Assign the current user as the author before saving
#             blog = form.save()
#             blog.author = request.user  # Assuming request.user is the logged-in user
#             blog.save()
#             messages.success(request, 'Blog published! Good job!')
#             return redirect('blogs:blogs')
#     else:
#         form = BlogForm(instance=blog)
    
#     return render(request, 'blogs/blog_form.html', {'form': form, 'categories':categories})

@login_required  # Ensure the user is authenticated
def create_blog(request, blog_id=None):
    categories = Blog.CATEGORIES
    if blog_id:
        blog = get_object_or_404(Blog, pk=blog_id)
    else:
        blog = None
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            # Assign the current user as the author before saving
            blog = form.save(commit=False)
            if not blog.author_id:  # Check if author is not set
                blog.author = request.user  # Assign the current user as the author
            blog.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Blog published! Good job!')
            return redirect('blogs:blogs')
    else:
        form = BlogForm(instance=blog)
    
    return render(request, 'blogs/blog_form.html', {'form': form, 'categories': categories})
def category(request, category):
    # Get blogs belonging to the specified category
    blogs = Blog.objects.filter(category__iexact=category)

    # Number of blogs to display per page
    per_page = 18  # You can adjust this as needed

    # Paginate blogs
    paginator = Paginator(blogs, per_page)

    # Get current page number from request, default to 1
    page_number = request.GET.get('page', 1)

    try:
        # Get blogs for the requested page
        blogs_page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        blogs_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results
        blogs_page = paginator.page(paginator.num_pages)

    return render(request, 'blogs/categories.html', {'category': category, 'blogs': blogs_page})

def featured(request):
    # Get blogs belonging to the specified category
    featured_blogs = Blog.objects.filter(featured=True)

    # Number of blogs to display per page
    per_page = 18  # You can adjust this as needed

    # Paginate blogs
    paginator = Paginator(featured_blogs, per_page)

    # Get current page number from request, default to 1
    page_number = request.GET.get('page', 1)

    try:
        # Get blogs for the requested page
        blogs_page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        blogs_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results
        blogs_page = paginator.page(paginator.num_pages)

    return render(request, 'blogs/featured.html', {'blogs': blogs_page})

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def search(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        filtered_blogs = Blog.objects.filter(title__icontains=title)[:24]
        
        return render(request, 'blogs/search.html', {'blogs': filtered_blogs})


def delete_blog(request, blog_id):
    # Retrieve the blog object from the database
    blog = get_object_or_404(Blog, pk=blog_id)

    # Check if the request method is POST (the form is submitted)
    if request.method == 'POST':
        if blog.author == request.user:
            blog.delete()
            messages.success(request, 'Blog deleted.')
        
            return redirect('blogs:blogs')

    # If the request method is not POST, render a confirmation template
    return render(request, 'blogs/index.html', {'blog': blog})

def delete_confirmation(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'blogs/delete_confirmation.html', {'blog':blog})

def user_blogs(request, username):
    # Retrieve the user object based on the username
    user = User.objects.get(username=username)
    
    # Retrieve the blogs authored by the user
    user_blogs = Blog.objects.filter(author=user)
    
    # Number of blogs to display per page
    per_page = 18  # You can adjust this as needed

    # Paginate blogs
    paginator = Paginator(user_blogs, per_page)

    # Get current page number from request, default to 1
    page_number = request.GET.get('page', 1)

    try:
        # Get blogs for the requested page
        blogs_page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        blogs_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results
        blogs_page = paginator.page(paginator.num_pages)
    
    # Pass the user blogs to the template context
    context = {
        'user': user,
        'blogs': blogs_page,
    }
    
    return render(request, 'blogs/user_blogs.html', context)

@login_required
def add_comment(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        blog_id = request.POST.get('blog_id') 
        
        if content and blog_id:
            user = request.user
            blog = Blog.objects.get(id=blog_id)
            
            # Create the comment object
            comment = Comment.objects.create(user=user, blog=blog, content=content)
            
            blog.save()
            
            # Optionally, you can perform additional actions, such as displaying a success message
            messages.success(request, 'Comment added!')
            
            # Redirect to the appropriate page
            return redirect('blogs:show-blog', pk=blog_id )  # Replace 'post_detail' with your actual view name
        
        else:
            # Handle the case where content or post_id is empty
            messages.error(request, 'Comment or post ID cannot be empty!')
            return render(request, 'blogs/blog.html', {'pk':blog_id})  # Render the same template where the form is included
    else:
        # If the request method is not POST, render the same template where the form is included
        return render(request, 'blogs/blog.html')