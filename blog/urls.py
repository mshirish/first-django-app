from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/create/', views.post_create, name='post_create'),        # must be before <slug>
    path('post/generate/', views.generate_post, name='generate_post'), # must be before <slug>
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),

    # API endpoints
    path('api/posts/', api_views.PostListAPI.as_view(), name='api_post_list'),
    path('api/posts/<slug:slug>/', api_views.PostDetailAPI.as_view(), name='api_post_detail'),
    path('api/generate/', api_views.GeneratePostAPI.as_view(), name='api_generate'),
]