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

@login_required
def create_blog(request, blog_id=None):
    categories = Blog.CATEGORIES
    if blog_id:
        blog = get_object_or_404(Blog, pk=blog_id)
    else:
        blog = None
    
    if request.method == 'POST':
        # Retrieve data from the request
        title = request.POST.get('title')
        pen_name = request.POST.get('pen_name')
        teaser = request.POST.get('teaser')
        content = request.POST.get('content')
        content2 = request.POST.get('content2')
        content3 = request.POST.get('content3')
        content4 = request.POST.get('content4')
        content5 = request.POST.get('content5')
        content6 = request.POST.get('content6')
        content7 = request.POST.get('content7')
        content8 = request.POST.get('content8')
        content9 = request.POST.get('content9')
        content10 = request.POST.get('content10')
        
        # Image fields
        image = request.FILES.get('image')
        image_end = request.FILES.get('image_end')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')
        image5 = request.FILES.get('image5')
        image6 = request.FILES.get('image6')
        image7 = request.FILES.get('image7')
        image8 = request.FILES.get('image8')
        image9 = request.FILES.get('image9')
        
        # Image caption fields
        image_end_caption = request.POST.get('image_end_caption')
        image2_caption = request.POST.get('image2_caption')
        image3_caption = request.POST.get('image3_caption')
        image4_caption = request.POST.get('image4_caption')
        image5_caption = request.POST.get('image5_caption')
        image6_caption = request.POST.get('image6_caption')
        image7_caption = request.POST.get('image7_caption')
        image8_caption = request.POST.get('image8_caption')
        image9_caption = request.POST.get('image9_caption')
        
        # Retrieve the category from the request
        category = request.POST.get('category')
        
        # Assuming the current user is the author
        author = request.user

        # Create a new Blog object
        blog = Blog(
            title=title,
            pen_name=pen_name,
            teaser=teaser,
            content=content,
            content2=content2,
            content3=content3,
            content4=content4,
            content5=content5,
            content6=content6,
            content7=content7,
            content8=content8,
            content9=content9,
            content10=content10,
            image=image,
            image_end=image_end,
            image2=image2,
            image3=image3,
            image4=image4,
            image5=image5,
            image6=image6,
            image7=image7,
            image8=image8,
            image9=image9,
            image_end_caption=image_end_caption,
            image2_caption=image2_caption,
            image3_caption=image3_caption,
            image4_caption=image4_caption,
            image5_caption=image5_caption,
            image6_caption=image6_caption,
            image7_caption=image7_caption,
            image8_caption=image8_caption,
            image9_caption=image9_caption,
            category=category, 
            author=author,
            # Add more fields as needed
        )
        
        # Save the blog object
        blog.save()
        
        messages.success(request, 'Blog published! Good job!')
        return redirect('blogs:blogs')
    
    return render(request, 'blogs/blog_form.html', {'categories': Blog.CATEGORIES})


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