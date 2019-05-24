from django.urls import path
from . import views as blog_views

urlpatterns = [
    # the articles view urls
    path("", blog_views.Articles.as_view(), name="articles"),
    path("articles/<filter_mode>/", blog_views.Articles.as_view(), name="articles-mode"),
    path("article/<int:pk>/", blog_views.SingleArticle.as_view(), name="single-article"),
    path("profile/<int:pk>/", blog_views.ProfileView.as_view(), name="profile-page"),

    # Article Crud
    path("article/create/", blog_views.CreateArticleView.as_view(), name="create-article"),
    path("article/<int:pk>/update/", blog_views.ArticleUpdate.as_view(), name="update-article"),
    path("article/<int:pk>/delete/", blog_views.ArticleDelete.as_view(), name="delete-article"),


    # Comment Crud
    path("comment/create/<int:article_pk>", blog_views.CommentCreate.as_view(), name="create-comment"),
    path("comment/update/<int:pk>/", blog_views.CommentUpdate.as_view(), name="update-comment"),
    path("comment/delete/<int:pk>/", blog_views.CommentDelete.as_view(), name="delete-comment"),

    # Reply Crud
    path("reply/create/<int:comment_pk>", blog_views.ReplyCreate.as_view(), name="create-reply"),
    path("reply/update/<int:pk>/", blog_views.ReplyUpdate.as_view(), name="update-reply"),
    path("reply/delete/<int:pk>/", blog_views.ReplyDelete.as_view(), name="delete-reply"),
]
