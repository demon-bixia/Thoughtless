from django import forms
from .models import Article, Comment, Reply


class ArticleCreateForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ("main_title", "header_image", "tags", "topic",)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ('text',)
