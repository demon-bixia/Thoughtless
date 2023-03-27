from django.db import models
from accounts.models import Profile
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


def upload_content(instance, filename):
    return f"{instance.author.pk}/article_headers/{filename}"


class Tag(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Article(models.Model):
    main_title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    header_image = models.ImageField(upload_to=upload_content)
    tags = models.ManyToManyField(Tag)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.main_title

    @property
    def get_lines(self):
        split_percentage = int()
        full_text = str()
        for paragraph in self.paragraph_set.all():
            split_percentage += 1
            full_text = full_text + paragraph.paragraph

        paragraph = self.paragraph_set.first().paragraph
        length = len(paragraph)
        return paragraph[:length // 2]


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return "comment"


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return "reply"


class Paragraph(models.Model):

    types = (
        ("1line", "one line paragraph"),
        ("split", "split paragraph")
    )

    type = models.CharField(max_length=20, default="1line", choices=types)
    paragraph = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.type

    @property
    def split1(self):
        length = len(self.paragraph)
        p1, p2 = self.paragraph[:length // 2], self.paragraph[length // 2:]
        return p1

    @property
    def split2(self):
        length = len(self.paragraph)
        p1, p2 = self.paragraph[:length // 2], self.paragraph[length // 2:]
        return p2
