from django.contrib import admin
from .models import Post, Comment, Like, Subscription

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'text', 'created_at', 'get_likes_count', 'get_comments_count']
    list_filter = ['created_at']
    search_fields = ['text', 'author__username']

    def get_likes_count(self, obj):
        return obj.likes.count()
    get_likes_count.short_description = 'Likes'

    def get_comments_count(self, obj):
        return obj.comments.count()
    get_comments_count.short_description = 'Comments'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'text', 'created_at']
    list_filter = ['created_at']
    search_fields = ['text', 'author__username', 'post__text']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__text']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['subscriber', 'target', 'created_at']
    list_filter = ['created_at']
    search_fields = ['subscriber__username', 'target__username']
