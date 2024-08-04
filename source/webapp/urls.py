from django.urls import path
from django.views.generic import RedirectView

from webapp.views.posts import PostListView, PostCreateView

app_name = 'webapp'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='webapp:index')),
    path('posts/', PostListView.as_view(), name='index'),
    path('create/', PostCreateView.as_view(), name='create_post'),
]
