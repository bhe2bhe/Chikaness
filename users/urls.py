from django.urls import path
from . import views
from .views import PostDeleteView, ProfilePostDeleteView

app_name = 'users'

urlpatterns = [
    path('',views.index,name='index'),
    path('comments/',views.comments,name='comments'),
    path('create_profile/', views.create_profile,name='create-profile'),
    path('follow', views.follow,name='follow'),
    path('<str:username>/followers', views.user_followers,name='user-followers'),
    path('<str:username>/following', views.user_following,name='user-following'),
    path('search/', views.search,name='search'),
    path('bulletin-board', views.post_to_bulletin_board, name="bulletin-board"),
    path('like-post', views.like_post, name="like-post"),
    path('likers/<uuid:pk>/', views.likers, name="likers"),
    path('add-comment', views.add_comment, name="add-comment"),
    path('delete-post/<uuid:pk>/', PostDeleteView.as_view(), name="delete-post"),
    path('profile-delete-post/<uuid:pk>/', ProfilePostDeleteView.as_view(), name="profile-delete-post"),
    path('profile-bulletin-board/<str:username>/', views.profile_bulletin_board, name="profile-bulletin-board"),
    path('bulletin-board-all/', views.show_bulletin_board, name='show-bulletin-board'),
    path('<str:username>/announcements/', views.user_announcements, name='user-announcements'),
]
