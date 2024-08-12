from blog.settings import BASE_DIR
from .models import Post, Like
from django.shortcuts import render


def PostList(request):
    posts = Post.objects.all()  # Получаем все посты
    post_likes = {post.id: Like.objects.filter(post=post).count() for post in
                  posts}  # Подсчитываем лайки для каждого поста

    context = {
        'posts': posts,
        'post_likes': post_likes,
    }

    return render(request, 'blog_app/post_list.html', context)
