from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import auth
from django.http import HttpResponseServerError
from .models import Profile, BulletinBoard, ProfileBulletinBoard, LikePost, FollowersCount, Comment
from blogs.models import Blog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain

def index(request):
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_object = User.objects.get(username=request.user.username)
            user_profile = Profile.objects.get(user=user_object)
        except User.DoesNotExist or Profile.DoesNotExist:
            pass
    
    # Retrieve all posts without pagination
    all_posts = BulletinBoard.objects.all().order_by('-created_at') 
    
    user_following_list = []
    feed = []
    
    user_following = FollowersCount.objects.filter(follower=request.user.username)
        
    for users in user_following:
        user_following_list.append(users.user)
        
    for usernames in user_following_list:
        feed_lists = BulletinBoard.objects.filter(user=usernames).order_by('-created_at')
        feed.append(feed_lists)
        
    # Include highlighted posts
    highlighted_posts = BulletinBoard.objects.filter(highlight=True)
    
    feed_list = list(chain(*feed)) + list(highlighted_posts)
    
    # Slice the first 20 posts
    first_20_posts = feed_list[:18]
    
    
    return render(request, 'users/index.html', {'user_profile': user_profile, 'posts': first_20_posts})

@login_required
def post_to_bulletin_board(request):
    if request.method == 'POST':
        user = request.user.username
        content = request.POST.get('content', '').strip()  # Using get() to handle the case where 'content' is missing
        
        # Get the uploaded image from the request.FILES dictionary
        image = request.FILES.get('image')
        
        if content == '' or not image:
            messages.error(request, 'Announcement empty or no image attached. Cannot be posted.', extra_tags='custom-error')
            return redirect('/')
        
        try:
            new_post = BulletinBoard.objects.create(user=user, content=content)
            if image:
                new_post.image = image
            new_post.save()
            messages.success(request, f'Posted!')
            # No need to call new_post.save() explicitly, create() already saves the object
            return redirect('bulletin-board-all/')
        except Exception as e:
            # Log the error or print it for debugging
            print(f"An error occurred while creating the bulletin board post: {e}")
            # You can return an error response if needed
            return HttpResponseServerError("An error occurred while creating the bulletin board post.")
    else:
        return redirect('/')

@login_required
def like_post(request):
    if request.method == 'POST':
        username = request.user
        post_id = request.POST.get('post_id')
        
        # Ensure that the post_id is valid and exists
        if post_id:
            # Retrieve the BulletinBoard object based on the post_id
            post = get_object_or_404(BulletinBoard, id=post_id)
            
            # Check if the user has already liked the post
            if username in post.liked.all():
                post.liked.remove(username)
                post.no_of_likes -= 1
                LikePost.objects.filter(post_id=post_id, username=username).delete()
            else:
                post.liked.add(username)
                post.no_of_likes += 1
                LikePost.objects.create(post_id=post_id, username=username)
            
            post.save()  # Save the changes to the post object
            return redirect('users:show-bulletin-board')  # Redirect to the homepage or previous page after liking/unliking
        else:
            # Handle the case where post_id is not provided
            return HttpResponse("Invalid post ID", status=400)
    else:
        # Return a response indicating that the method is not allowed
        return HttpResponse("Method Not Allowed", status=405)

def likers(request, pk):
    # Get the BulletinBoard object with the given primary key
    post = get_object_or_404(BulletinBoard, id=pk)
    
    # Check if the post has been liked by any users
    if hasattr(post, 'liked'):
        likers = post.liked.all()
    else:
        likers = []
        
    # Fetch comments related to the specific post
    comments = Comment.objects.filter(post=post)

    return render(request, 'users/likers.html', {'likers': likers, 'post':post, 'comments':comments})

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = BulletinBoard
    success_url = reverse_lazy('users:show-bulletin-board')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        # Get the object to be deleted
        self.object = self.get_object()
        
        # Check if the current user is the owner of the post
        if self.object.user == self.request.user:
            # Delete the post
            self.object.delete()

            # Add success message
            messages.success(self.request, f'Announcement successfully deleted.')
            
        else:
            # Add error message
            messages.error(self.request,f'You do not have permission to delete this announcement.')
            
            
        return HttpResponseRedirect(self.get_success_url())

class ProfilePostDeleteView(LoginRequiredMixin, DeleteView):
    model = ProfileBulletinBoard
    # success_url = reverse_lazy('profile')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        # Get the object to be deleted
        self.object = self.get_object()
        
        # Check if the current user is the owner of the post
        if self.object.user == self.request.user:
            # Delete the post
            self.object.delete()

            # Add success message
            messages.success(self.request, f'Announcement deleted.')
            
        else:
            # Add error message
            messages.error(self.request,f'You do not have permission to delete this announcement.')
            
            
        return redirect('profile',username=self.object.profile.user.username)
    
    def get_success_url(self):
        # Redirect to the profile page of the user whose announcement was deleted
        return reverse_lazy('profile', kwargs={'username': self.object.profile.user.username})
    
def user_announcements(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    announcement_list = BulletinBoard.objects.filter(user=username).order_by('-created_at')
    
    paginator = Paginator(announcement_list, 18)
    page_number = request.GET.get('page', 1)  

    try:
        announcements = paginator.page(page_number)
    except PageNotAnInteger:
        announcements = paginator.page(1)
    except EmptyPage:
        announcements = paginator.page(paginator.num_pages)
    
    return render(request, 'users/user-announcements.html', {'announcements': announcements, 'username': username, 'profile':profile})
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')  # Retrieve username
            password = form.cleaned_data.get('password1')  # Retrieve password
            form.save()
            
            user = User.objects.get(username=username)
            user_login = auth.authenticate(username=username, password=password)
            auth.login(request, user_login)
            
            Profile.objects.create(user=user)  # Create a Profile object for the user
            
            messages.success(request,f'Welcome <span style="font-weight:bold;">{username}</span>! You have successfully created a profile.')
            return redirect('users:create-profile')
        
    else:
        form = UserCreationForm()
        
    return render(request, 'users/register.html',{'form':form})

def comments(request):
    return render(request,'users/comments.html')

def profile(request, username):
    # Retrieve the user being viewed
    profile_user = get_object_or_404(User, username=username)

    # Retrieve the profile associated with the user being viewed
    profile = get_object_or_404(Profile, user=profile_user)
    
    # Retrieve the count of blogs associated with the user
    user_blog_count = Blog.objects.filter(author=profile_user).count()    
    
    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = BulletinBoard.objects.filter(user=username)
    user_posts_length = len(user_posts)
    user_followers = FollowersCount.objects.filter(follower=username)
    user_followers_length = len(user_followers)
    user_following = FollowersCount.objects.filter(user=username)
    user_following_length = len(user_following)
    
    follower = request.user.username
    user = username
    
    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'  
    else :
        button_text = 'Follow'
    
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_posts_length': user_posts_length,
        'user_followers': user_followers,
        'user_followers_length': user_followers_length,
        'user_following': user_following,
        'user_following_length': user_following_length,
        'button_text': button_text,
        'profile_user': profile_user,
        'profile': profile,
        'user_blog_count': user_blog_count, 
    }

    # Retrieve the posts associated with the user being viewed
    posts = ProfileBulletinBoard.objects.filter(user=profile_user).order_by('created_at')

    return render(request, 'users/profile.html', context)   

@login_required
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            messages.success(request, f'You have unfollowed {user}.')
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            messages.success(request, f'You are now following {user}.')
            
        return redirect('profile', username=user) 
        
    else:
        return redirect('users:index')
    
def user_followers(request,username):
    profile = get_object_or_404(Profile, user__username=username)
    
    # Fetch the usernames of followers for the given user
    follower_usernames = FollowersCount.objects.filter(user=username).values_list('follower', flat=True)
    
    # Fetch the profiles of followers based on their usernames
    followers_profiles = Profile.objects.filter(user__username__in=follower_usernames)

    return render(request, 'users/user-followers.html', {'followers_profiles': followers_profiles, 'username': username, 'profile': profile})

def user_following(request,username):
    profile = get_object_or_404(Profile, user__username=username)
    
    # Fetch the usernames of followers for the given user
    following_usernames = FollowersCount.objects.filter(follower=username).values_list('user', flat=True)
    
    # Fetch the profiles of followers based on their usernames
    following = Profile.objects.filter(user__username__in=following_usernames)

    return render(request, 'users/user-following.html', {'following': following, 'username': username, 'profile': profile})

def search(request):
    if request.method == 'POST':
        username = request.POST['username']
        username_objects = User.objects.filter(username__icontains=username)
        
        username_profile_list = []
        
        for user_obj in username_objects:
            try:
                profile = Profile.objects.get(user=user_obj)
                username_profile_list.append(profile)
            except Profile.DoesNotExist:
                pass  # Handle the case where a profile for the user does not exist
            
    return render(request, 'users/search.html', {'username_profile_list': username_profile_list})
        

@login_required
def create_profile(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        image = request.FILES.get('image')
        motto = request.POST.get('motto')
        about_yourself = request.POST.get('about_yourself')
        q1 = request.POST.get('q1')
        q2 = request.POST.get('q2')
        q3 = request.POST.get('q3')
        q4 = request.POST.get('q4')
        
        # check if image is provided
        if image:
            user_profile.profile_pic = image
            
        user_profile.motto = motto
        user_profile.about_yourself = about_yourself
        user_profile.q1 = q1
        user_profile.q2 = q2
        user_profile.q3 = q3
        user_profile.q4 = q4
        user_profile.save()
            
        messages.success(request, 'Profile edited.')
        return redirect('profile', username=request.user.username)
        
    return render(request,'users/profile_form.html', {'user_profile': user_profile})

@login_required
def profile_bulletin_board(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    profile_post = ProfileBulletinBoard.objects.all()

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            try:
                new_post = ProfileBulletinBoard.objects.create(user=request.user, profile=profile, content=content)
                messages.success(request, 'Message posted!')
            except Exception as e:
                messages.error(request, f'Error occurred while creating the post: {str(e)}')
        else:
            messages.error(request, 'You cannot post an empty announcement.')    
    
        return redirect('profile', username=username)
    return render(request, '/<str:username>', {'profile': profile, 'profile_post': profile_post})

def show_bulletin_board(request):
    try:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)
    except User.DoesNotExist:
        # Handle User.DoesNotExist exception
        user_profile = None
    except Profile.DoesNotExist:
        # Handle Profile.DoesNotExist exception
        user_profile = None

    # all_posts = BulletinBoard.objects.all().order_by('-created_at') 
    
    user_following_list = []
    feed = []
    
    user_following = FollowersCount.objects.filter(follower=request.user.username)
    
    for users in user_following:
        user_following_list.append(users.user)
        
    for usernames in user_following_list:
        feed_lists = BulletinBoard.objects.filter(user=usernames)
        feed.append(feed_lists)
        
    user_posts = BulletinBoard.objects.filter(user=request.user)
    
    # Include highlighted posts
    highlighted_posts = BulletinBoard.objects.filter(highlight=True)
    
    # Combine feed and highlighted posts
    feed_list = list(chain(*feed)) + list(user_posts) + list(highlighted_posts)
    
    # Order posts by creation date in descending order
    feed_list = sorted(feed_list, key=lambda x: x.created_at, reverse=True)
    
    if not feed_list and request.user.is_authenticated:
        
        messages.info(request, "Follow people to start viewing their announcements.")
    
    # Paginate 
    paginator = Paginator(feed_list, 18)
    page_number = request.GET.get('page', 1)  

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'users/bulletin-board.html', {'user_profile': user_profile, 'posts': posts})

def logout_view(request):
    logout(request)
    
    return render(request,'users/logout.html')

@login_required
def add_comment(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        post_id = request.POST.get('post_id')  # Assuming 'post_id' is submitted with the form
        
        if content and post_id:
            user = request.user
            post = BulletinBoard.objects.get(id=post_id)
            
            # Create the comment object
            comment = Comment.objects.create(user=user, post=post, content=content)
            
            post.no_of_comments += 1
            
            post.save()
            
            # Optionally, you can perform additional actions, such as displaying a success message
            messages.success(request, 'Comment added!')
            
            # Redirect to the appropriate page
            return redirect('users:likers', pk=post_id )  # Replace 'post_detail' with your actual view name
        
        else:
            # Handle the case where content or post_id is empty
            messages.error(request, 'Comment or post ID cannot be empty!')
            return render(request, 'users/likers.html', {'pk':post_id})  # Render the same template where the form is included
    else:
        # If the request method is not POST, render the same template where the form is included
        return render(request, 'users/likers.html')