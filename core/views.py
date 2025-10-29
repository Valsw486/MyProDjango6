from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Post, Like, Comment, Subscription
from .forms import PostForm, CommentForm


def home(request):
    # Если пользователь авторизован, показываем посты от подписок
    if request.user.is_authenticated:
        # Получаем ID пользователей, на которых подписан текущий пользователь
        subscriptions = Subscription.objects.filter(subscriber=request.user).values_list('target_id', flat=True)
        # Добавляем посты самого пользователя
        subscriptions_list = list(subscriptions) + [request.user.id]
        posts = Post.objects.filter(author_id__in=subscriptions_list).order_by('-created_at')
    else:
        # Для неавторизованных показываем все посты
        posts = Post.objects.all().order_by('-created_at')

    # Обработка создания поста
    if request.method == 'POST' and request.user.is_authenticated:
        if 'text' in request.POST:  # Это форма поста
            text = request.POST.get('text')
            image = request.FILES.get('image')

            if text:
                post = Post.objects.create(
                    author=request.user,
                    text=text,
                    image=image
                )
                messages.success(request, 'Post created successfully!')
                return redirect('home')

    return render(request, 'core/home.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'core/create_post.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        messages.error(request, 'You can only edit your own posts!')
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('home')
    else:
        form = PostForm(instance=post)

    return render(request, 'core/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        messages.error(request, 'You can only delete your own posts!')
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')

    return render(request, 'core/delete_post.html', {'post': post})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')

    return redirect('home')


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        messages.error(request, 'You can only delete your own comments!')
        return redirect('home')

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')

    return redirect('home')


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count()
        })

    return redirect('home')


@login_required
def subscribe(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        messages.error(request, 'You cannot subscribe to yourself!')
        return redirect('home')

    subscription, created = Subscription.objects.get_or_create(
        subscriber=request.user,
        target=target_user
    )

    if created:
        messages.success(request, f'You have subscribed to {target_user.username}!')
    else:
        messages.info(request, f'You are already subscribed to {target_user.username}')

    return redirect('home')


@login_required
def unsubscribe(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    subscription = Subscription.objects.filter(
        subscriber=request.user,
        target=target_user
    )

    if subscription.exists():
        subscription.delete()
        messages.success(request, f'You have unsubscribed from {target_user.username}')
    else:
        messages.error(request, f'You are not subscribed to {target_user.username}')

    return redirect('home')


@login_required
def subscriptions_list(request):
    # Пользователи, на которых подписан текущий пользователь
    subscriptions = Subscription.objects.filter(subscriber=request.user).select_related('target')
    return render(request, 'core/subscriptions_list.html', {'subscriptions': subscriptions})


@login_required
def subscribers_list(request):
    # Пользователи, которые подписаны на текущего пользователя
    subscribers = Subscription.objects.filter(target=request.user).select_related('subscriber')
    return render(request, 'core/subscribers_list.html', {'subscribers': subscribers})


@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    is_subscribed = Subscription.objects.filter(subscriber=request.user, target=user).exists()

    context = {
        'profile_user': user,
        'posts': posts,
        'is_subscribed': is_subscribed,
        'posts_count': posts.count(),
        'subscribers_count': Subscription.objects.filter(target=user).count(),
        'subscriptions_count': Subscription.objects.filter(subscriber=user).count(),
    }

    return render(request, 'core/user_profile.html', context)


def explore_users(request):
    # Показываем всех пользователей кроме текущего
    users = User.objects.all()
    if request.user.is_authenticated:
        users = users.exclude(id=request.user.id)

    # Для авторизованных пользователей добавляем информацию о подписках
    if request.user.is_authenticated:
        subscribed_users = Subscription.objects.filter(
            subscriber=request.user
        ).values_list('target_id', flat=True)

        for user in users:
            user.is_subscribed = user.id in subscribed_users

    return render(request, 'core/explore_users.html', {'users': users})