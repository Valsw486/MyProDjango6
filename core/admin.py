from django.contrib import admin
from .models import Post, Comment, Like, Subscription


class CommentInline(admin.TabularInline):
    """Show comments directly inside the post edit page."""
    model = Comment
    extra = 0
    readonly_fields = ['created_at']
    fields = ['author', 'text', 'created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'author', 'short_text',
        'created_at', 'get_likes_count', 'get_comments_count'
    ]
    list_filter = ['created_at', 'author']
    search_fields = ['text', 'author__username']
    date_hierarchy = 'created_at'
    list_select_related = ['author']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CommentInline]
    list_per_page = 25
    ordering = ['-created_at']

    @admin.display(description='Text')
    def short_text(self, obj):
        """Short preview of the post text."""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    @admin.display(description='Likes')
    def get_likes_count(self, obj):
        return obj.likes.count()

    @admin.display(description='Comments')
    def get_comments_count(self, obj):
        return obj.comments.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'post', 'short_text', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['text', 'author__username', 'post__text']
    date_hierarchy = 'created_at'
    list_select_related = ['author', 'post']
    readonly_fields = ['created_at']
    list_per_page = 25

    @admin.display(description='Text')
    def short_text(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__text']
    date_hierarchy = 'created_at'
    list_select_related = ['user', 'post']
    readonly_fields = ['created_at']
    list_per_page = 25


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'subscriber', 'target', 'created_at']
    list_filter = ['created_at']
    search_fields = ['subscriber__username', 'target__username']
    date_hierarchy = 'created_at'
    list_select_related = ['subscriber', 'target']
    readonly_fields = ['created_at']
    list_per_page = 25
    