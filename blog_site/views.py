from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import Article, Paragraph, Comment, Reply
from django.core.paginator import Paginator
from .forms import ArticleCreateForm, CommentForm, ReplyForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from accounts.models import Profile
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# noinspection PyMethodMayBeStatic
# the Article list view only accept get requests
# filters the articles query set and returns a paginated
# article list
class Articles(View):
    filter_content = "featured"
    template_name = "blog_site/index-no-grid.html"
    p_queryset = None

    def get(self, request, filter_mode=None):
        if filter_mode:
            self.filter_content = filter_mode
        article_list = self.get_articles()
        paginator = self.pagination(article_list)
        page = request.GET.get('page')
        self.p_queryset = paginator.get_page(page)
        context = self.get_context_data()
        context['pre_url'] = request.META.get('HTTP_REFER')
        if self.filter_content == "All":
            self.template_name = "blog_site/index-grid.html"
        return render(request, self.template_name, context)

    # returns the query set for the Article
    def get_articles(self):
        if self.filter_content == "featured":
            articles = Article.objects.filter(featured=True).order_by('-date')
        else:
            articles = Article.objects.order_by('-date')
        return articles

    # returns the paginated articles list
    def pagination(self, queryset):
        if self.filter_content == "featured":
            paginator = Paginator(queryset, 3)
        else:
            paginator = Paginator(queryset, 5)
        return paginator

    # returns the context data to be rendered
    def get_context_data(self):
        return {"articles": self.p_queryset}


class SingleArticle(View):
    template_name = "blog_site/index-single-post.html"
    context = dict()

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        self.context['article'] = article
        self.context['profile'] = request.user.profile
        return render(request, self.template_name, self.context)


@method_decorator(login_required, name='dispatch')
class CreateArticleView(View):
    template_name = "blog_site/forms/ArticleCreate.html"
    form_class = ArticleCreateForm
    context = dict()

    # renders the create form
    def get(self, request):
        form = self.form_class()
        self.context = self.get_context(form)
        return render(request, self.template_name, self.context)

    # creates and saves the Article object
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        self.context = self.get_context(form)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user.profile
            article.save()
            counter = 1
            self.create_paragraphs(request=request, article=article, counter=counter)
            return redirect('articles-mode', filter_mode="All")
        else:
            return render(request, self.template_name, self.context)

    # noinspection PyMethodMayBeStatic
    # saves the article paragraphs one by one
    # looping the request.POST dict
    def create_paragraphs(self, request, article, counter):
        for key, value in request.POST.items():
            if key == f"text_area_{counter}":
                p = Paragraph(type="1line", paragraph=value, article=article)
                p.save()
                counter += 1
            if key == f"text_area_split_{counter}":
                p = Paragraph(type="split", paragraph=value, article=article)
                p.save()
                counter += 1
        return None

    # gets the context dic and adds the form into it
    def get_context(self, form):
        self.context['form'] = form
        return self.context


@method_decorator(login_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ArticleUpdate(View):
    form_class = ArticleCreateForm
    template_name = "blog_site/forms/ArticleUpdate.html"
    context = dict()

    # noinspection PyMethodOverriding
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        form = self.form_class(instance=article)
        count = article.paragraph_set.count()
        self.context['count'] = count
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    # noinspection PyMethodOverriding
    def post(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        form = self.form_class(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save()
            new_count = int(request.POST.get('input_counter'))
            o_count = article.paragraph_set.count()
            if new_count > o_count:
                self.create_paragraphs(request, article, o_count)
            self.update_paragraphs(request, article)
            return redirect('articles-mode', filter_mode="All")
        else:
            self.context['form'] = form
            self.context['count'] = article.paragraph_set.count()
            return render(request, self.template_name, self.context)

    def create_paragraphs(self, request, article, o_count):
        counter = o_count + 1
        for key, value in request.POST.items():
            if key == f"text_area_{counter}":
                paragraph = Paragraph(paragraph=value, article=article, type="1line")
                paragraph.save()
                counter += 1
            if key == f"text_area_split_{counter}":
                paragraph = Paragraph(paragraph=value, article=article, type="split")
                paragraph.save()
                counter += 1
        return counter

    def update_paragraphs(self, request, article):
        counter = 1
        for paragraph in article.paragraph_set.all():
            if request.POST.get(f"text_area_{counter}"):
                paragraph.paragraph = request.POST.get(f"text_area_{counter}")
                counter += 1
            if request.POST.get(f"text_area_split_{counter}"):
                paragraph.paragraph = request.POST.get(f"text_area_split_{counter}")
                counter += 1
            paragraph.save()
        return counter


@method_decorator(login_required, name='dispatch')
class ArticleDelete(View):

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        id = article.author.pk
        article.delete()
        return redirect('profile-page', pk=id)


@method_decorator(login_required, name='dispatch')
class CommentCreate(View):
    data = dict()
    template_name = "blog_site/part/comment_partial.html"

    def post(self, request, article_pk):
        comment_text = request.POST.get("text")
        author = request.user.profile
        article = get_object_or_404(Article, pk=article_pk)
        comment = Comment(article=article, author=author, text=comment_text)
        comment.save()
        html_content = render_to_string(self.template_name, {
            "comment": comment,
            'profile': request.user.profile
        })
        self.data['successful'] = True
        self.data['html_content'] = html_content
        return JsonResponse(self.data)


@method_decorator(login_required, name='dispatch')
class CommentUpdate(View):
    form_class = CommentForm
    form_template = "blog_site/part/comment_update_partial.html"
    template_name = "blog_site/part/comment_partial.html"
    data = dict()

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        form = self.form_class(instance=comment)
        html_form = render_to_string(self.form_template, {
            "comment": comment,
            "form": form
        }, request=request)
        self.data['successful'] = True
        self.data['html_form'] = html_form
        return JsonResponse(self.data)

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        form = self.form_class(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            html_content = render_to_string(self.template_name, {"comment": comment, 'profile': request.user.profile})
            self.data['successful'] = True
            self.data['html_content'] = html_content
            return JsonResponse(self.data)
        else:
            self.data['successful'] = False
            html_form = render_to_string(self.form_template, {'form': form, 'comment': comment})
            self.data['html_form'] = html_form
        return JsonResponse(self.data)


@method_decorator(login_required, name='dispatch')
class CommentDelete(View):
    data = dict()

    def get(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            self.data['successful'] = True
            self.data['message'] = "Comment Deleted"
        except Comment.DoesNotExist:
            self.data['successful'] = False
            self.data['message'] = "comment not found"
        return JsonResponse(self.data)


@method_decorator(login_required, name='dispatch')
class ReplyCreate(View):
    template_name = "blog_site/part/reply_partial.html"
    form_template = "blog_site/part/reply_partial_create.html"
    form_class = ReplyForm
    data = dict()

    def get(self, request, comment_pk=None):
        form = self.form_class()
        try:
            comment = Comment.objects.get(pk=comment_pk)
            html_form = render_to_string(self.form_template, {'form': form, 'comment': comment}, request=request)
            self.data['html_form'] = html_form
            self.data['successful'] = True
        except Comment.DoesNotExist:
            self.data['successful'] = False

        return JsonResponse(self.data)

    def post(self, request, comment_pk=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            try:
                comment = Comment.objects.get(pk=comment_pk)
                reply.comment = comment
                reply.author = request.user.profile
                reply.save()
                self.data['successful'] = True
                self.data['html_content'] = render_to_string(self.template_name, {'reply': reply,
                                                                                  'profile': request.user.profile
                                                                                  }, request=request)
            except Comment.DoesNotExist:
                self.data['successful'] = False
        else:
            self.data['successful'] = False
            self.data['html_form'] = render_to_string(self.form_template, {'form': form})
        return JsonResponse(self.data)


@method_decorator(login_required, name='dispatch')
class ReplyUpdate(View):
    form_class = ReplyForm
    data = dict()
    template_name = "blog_site/part/reply_partial.html"
    form_template = "blog_site/part/reply_partial_update.html"

    def get(self, request, pk):
        try:
            reply = Reply.objects.get(pk=pk)
            form = self.form_class(instance=reply)
            html_form = render_to_string(self.form_template, {'form': form, 'reply': reply}, request=request)
            self.data['html_form'] = html_form
            self.data['successful'] = True
        except Reply.DoesNotExist:
            self.data['successful'] = False
        return JsonResponse(self.data)

    def post(self, request, pk):
        try:
            reply = Reply.objects.get(pk=pk)
            form = self.form_class(request.POST, instance=reply)
            if form.is_valid():
                form.save()
                self.data['successful'] = True
                self.data['html_content'] = render_to_string(self.template_name, {"reply": reply,
                                                                                  'profile': request.user.profile},
                                                             request=request)
            else:
                self.data['successful'] = False
                self.data['html_form'] = render_to_string(self.form_template, {'form': form, 'reply': reply},
                                                          request=request)
        except Reply.DoesNotExist:
            self.data['successful'] = False

        return JsonResponse(self.data)


@method_decorator(login_required, name='dispatch')
class ReplyDelete(View):
    data = dict()

    def get(self, request, pk):
        try:
            reply = Reply.objects.get(pk=pk)
            reply.delete()
            self.data['successful'] = True
            self.data['message'] = "Comment Deleted"
        except Reply.DoesNotExist:
            self.data['successful'] = False
            self.data['message'] = "comment not found"
        return JsonResponse(self.data)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = "blog_site/user_profile.html"

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        articles = Article.objects.filter(author=profile)
        return render(request, self.template_name, {"profile": profile, "articles": articles})
