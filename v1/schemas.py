from ninja import Schema, ModelSchema
from v1.models import User, Article, Comment


class UserSchema(Schema):
    class Config:
        model = User
        model_fields = '__all__'


class UserCreate(Schema):
    username: str
    password: str


class ArticleSchema(ModelSchema):
    class Config:
        model = Article
        model_fields = '__all__'


class CreateUpdateArticleSchema(ModelSchema):
    class Config:
        model = Article
        model_fields = ['title', 'content']


class CommentSchema(ModelSchema):
    class Config:
        model = Comment
        model_fields = '__all__'


class UpdateCreateCommentSchema(ModelSchema):
    class Config:
        model = Comment
        model_fields = ['content', ]