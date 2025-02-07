from django.contrib.auth import get_user_model
from ninja import NinjaAPI
from .models import Article, Comment, User
from django.contrib.auth.hashers import make_password
from ninja.security import HttpBearer
from .schemas import (UserCreate, ArticleSchema, CreateUpdateArticleSchema, CommentSchema,
                      UpdateCreateCommentSchema)
import secrets


api = NinjaAPI()


class TokenAuth(HttpBearer):
    def authenticate(self, request, token: str):
        try:
            user = get_user_model().objects.get(token=token)
            return user
        except User.DoesNotExist:
            return None


@api.get("/bearer", auth=TokenAuth(), tags=['Аккаунт'])
def bearer(request):
    return {"token": request.auth}


@api.post('/register/',  tags=['Аккаунт'], summary='Регистрация')
def register(request, payload: UserCreate):
    user = User(username=payload.username)
    user.password = make_password(payload.password)
    user.token = secrets.token_hex(128)
    user.save()
    return {"token": user.token}


@api.post('/login/',  tags=['Аккаунт'], summary='Авторизация')
def login(request, payload: UserCreate):
    try:
        user = User.objects.get(username=payload.username)
        if user.check_password(payload.password):
            return {"token": user.token}
        return {"error": 'Неверные учетные данные'}
    except User.DoesNotExist:
        return {"error": 'Пользователь не найден'}


@api.get('/articles/', response=list[ArticleSchema],  tags=['Статьи'], summary='Просмотр статей')
def get_articles(request):
    articles = Article.objects.all()
    return articles


@api.post('/articles', response=ArticleSchema, auth=TokenAuth(), tags=['Статьи'], summary='Создание статей')
def create_article(request, article: CreateUpdateArticleSchema):
    article_instance = Article.objects.create(**article.dict(), author=request.auth)
    return article_instance


@api.put('/articles/{article_id}', response=ArticleSchema, auth=TokenAuth(), tags=['Статьи'],
         summary='Редактирование статьи')
def update_article(request, article_id: int, article: ArticleSchema):
    try:
        article_instance = Article.objects.get(id=article_id)
    except:
        return {'error': 'Статья не найдена'}

    if article_instance.author != request.auth:
        return {'error': 'У вас нет прав на редактирование этой статьи'}

    for attr, value in article.dict().items():
        setattr(article_instance, attr, value)

    article_instance.save()
    return article_instance


@api.delete('/articles/{article_id}', auth=TokenAuth(), tags=['Статьи'], summary='Удаление статьи')
def delete_article(request, article_id: int):
    try:
        article_instance = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        return {'error': 'Статья не найдена'}

    if article_instance.author != request.auth:
        return {'error': 'У вас нет разрешения на удаление этой статьи'}

    article_instance.delete()
    return {'message': 'Статья удалена'}


@api.get('/articles/{article_id}/comments/', response=list[CommentSchema], tags=['Комментарии'],
         summary='Просмотр комментариев')
def get_comments(request, article_id: int):
    comments = Comment.objects.filter(article_id=article_id)
    return comments


@api.post('/articles/{article_id}/comments', response=CommentSchema, auth=TokenAuth(), tags=['Комментарии'],
         summary='Написать комментарий к статье')
def create_comment(request, article_id: int, comment: UpdateCreateCommentSchema):
    comment_instance = Comment.objects.create(**comment.dict(), author=request.auth, article_id=article_id)
    return comment_instance


@api.put('/comments/{comment_id}', response=CommentSchema, auth=TokenAuth(), tags=['Комментарии'],
                   summary='Редактирование комментария')
def update_comment(request, comment_id: int, comment: UpdateCreateCommentSchema):
    try:
        comment_instance = Comment.objects.get(id=comment_id)
    except:
        return {'error': 'Не найден комментарий'}

    if comment_instance.author != request.auth:
        return {'error': 'У вас нет прав на редактирование этого комментария'}

    for attr, value in comment.dict().items():
        setattr(comment_instance, attr, value)

    comment_instance.save()
    return comment_instance


@api.delete('/comments/{comment_id}', auth=TokenAuth(), tags=['Комментарии'],
            summary='Редактировать комментарий')
def delete_comment(request, comment_id: int):
    try:
        comment_instance = Comment.objects.get(id=comment_id)
    except:
        return {'error': 'Не найден комментарий'}

    if comment_instance.author != request.auth:
        return {'error': 'У вас нет разрешения удалять этот комментарий'}

    comment_instance.delete()
    return {'message': 'Комментарий удалён'}