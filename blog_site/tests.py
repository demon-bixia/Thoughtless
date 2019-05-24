from django.test import TestCase
from .models import Topic, Article, Comment, Tag, Reply
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()


# Create your tests here.
class TestBlogModels(TestCase):

    def setUp(self):
        self.topic = Topic(name="Development")
        self.topic.save()
        self.tag = Tag(name="Press Release")
        self.tag.save()
        self.user = User(username="test", email="test@test.com", password="test")
        self.user.save()
        self.author = Profile(user=self.user, job="Tech-lead", bio="web dev from sudan")
        self.author.save()
        self.article = Article(main_title="Making Python", author=self.author, topic=self.topic,
                               content="Hello World")
        self.article.save()
        self.article.tags.add(self.tag)
        self.author.save()
        self.comment = Comment(article=self.article, text="What is python any way")
        self.comment.save()
        self.reply = Reply(comment=self.comment, text="a programming language")
        self.reply.save()

    def test_topic_creation(self):
        self.assertEqual(self.topic.name, "Development")

    def test_article_creation(self):
        self.assertEqual(self.article.main_title, "Making Python")
        self.assertEqual(self.article.author, self.author)
        self.assertEqual(self.article.topic.id, self.topic.id)
        self.assertEqual(self.article.content,  "Hello World")

    def test_tags(self):
        tag2 = Tag(name="Tech")
        tag2.save()
        self.article.tags.add(tag2)
        self.assertEqual(self.article.tags.count(), 2)

    def test_comments(self):
        self.assertEqual(self.comment.article.id, self.article.id)
        self.assertEqual(self.comment.text, "What is python any way")

    def test_replies(self):
        self.assertEqual(self.reply.comment.id, self.comment.id)
        self.assertEqual(self.reply.text, "a programming language")
