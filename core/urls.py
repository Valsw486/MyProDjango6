from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/new/', views.create_post, name='create-post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit-post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete-post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add-comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete-comment'),
    path('post/<int:post_id>/like/', views.like_post, name='like-post'),

    # Подписки
    path('user/<int:user_id>/subscribe/', views.subscribe, name='subscribe'),
    path('user/<int:user_id>/unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('subscriptions/', views.subscriptions_list, name='subscriptions-list'),
    path('subscribers/', views.subscribers_list, name='subscribers-list'),
    path('user/<int:user_id>/', views.user_profile, name='user-profile'),
    path('explore/', views.explore_users, name='explore-users'),
]



