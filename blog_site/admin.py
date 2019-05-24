from django.contrib import admin
from .models import Tag, Reply, Article, Comment, Topic, Paragraph


admin.site.register(Topic)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Paragraph)
admin.site.register(Comment)
admin.site.register(Reply)
