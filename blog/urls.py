from . import views
from django.urls import path


urlpatterns = [
    path("", views.PostList.as_view(), name='home'),
    path('category/<slug:slug>/', views.PostList.as_view(), name='category_list'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like')
]