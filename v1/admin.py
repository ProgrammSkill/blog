from django.contrib import admin
from v1.models import User, Article, Comment, Categories


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'token']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'author']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'content', 'author']


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['title',]

