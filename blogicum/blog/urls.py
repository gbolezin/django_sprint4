from django.urls import path, include

from . import views

app_name = 'blog'

post_urls = [
    path('create/',
         views.PostCreateView.as_view(),
         name='create_post'),
    path('<int:pk>/',
         views.PostDetailView.as_view(),
         name='post_detail'),
    path('<int:pk>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'
         ),
    path('<int:pk>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'
         ),
    path('<int:pk>/comment/',
         views.CommentCreateView.as_view(),
         name='add_comment'
         ),
    path('<int:post_id>/edit_comment/<int:comment_id>/',
         views.CommentUpdateView.as_view(),
         name='edit_comment'
         ),
    path('<int:post_id>/delete_comment/<int:comment_id>/',
         views.CommentDeleteView.as_view(),
         name='delete_comment'
         ),
]

profile_urls = [
    path('edit/',
         views.ProfileUpdateView.as_view(),
         name='edit_profile'),
    path('<str:username>/',
         views.ProfileDetailView.as_view(),
         name='profile'),
]

category_urls = [
    path('<slug:slug>/',
         views.CategoryDetailView.as_view(), name='category_posts'),
]

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('posts/', include(post_urls)),
    path('profile/', include(profile_urls)),
    path('category/', include(category_urls)),
]
