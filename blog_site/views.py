import re

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import View

from accounts.forms import ProfileUpdateForm, ProfilePicUpdateForm
from .exceptions import HasNoProfile
from .forms import ArticleCreateForm, CommentForm, ReplyForm, SearchForm
from .models import Article, Paragraph, Comment, Reply


# the Article list view only accept get requests
# filters the articles query set and returns a paginated
# article list
class Articles(View):
    filter_content = "Featured"
    template_name = "blog_site/index-no-grid.html"
    p_queryset = None

    def get(self, request, filter_mode=None):
        if filter_mode:
            self.filter_content = filter_mode

        article_list = self.get_articles()  # get all Articles
        # create a paginator for articles querySet
        paginator = self.pagination(article_list)
        page = request.GET.get('page')  # get current page from request
        # get paginated queryset according to current page
        self.p_queryset = paginator.get_page(page)

        context = self.get_context_data()
        context['pre_url'] = request.META.get('HTTP_REFER')  # get the pre url

        if self.filter_content == "All":
            self.template_name = "blog_site/index-grid.html"
        elif self.filter_content == "Featured":
            self.template_name = "blog_site/index-no-grid.html"

        return render(request, self.template_name, context)

    # returns the query set for the Article
    def get_articles(self):
        if self.filter_content == "Featured":
            articles = Article.objects.filter(featured=True).order_by('-date')
        else:
            articles = Article.objects.order_by('-date')
        return articles

    # returns the paginated articles list

    def pagination(self, queryset):
        if self.filter_content == "Featured":
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
        try:
            # if profile dose not exist raise custom exception
            if not hasattr(request.user, "profile"):
                raise HasNoProfile("user has no profile",
                                   "blog_site/views.py", "SingleArticle")
            else:
                # add profile to context
                self.context['profile'] = request.user.profile
        except HasNoProfile:
            # make profile value None
            self.context['profile'] = None

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

            # add tags
            for tag in form.cleaned_data.get("tags"):
                article.tags.add(tag)

            counter = 1
            self.create_paragraphs(
                request=request, article=article, counter=counter)
            return redirect('articles-mode', filter_mode="All")
        else:
            return render(request, self.template_name, self.context)

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
class ArticleUpdate(View):
    form_class = ArticleCreateForm
    template_name = "blog_site/forms/ArticleUpdate.html"
    context = dict()

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        form = self.form_class(instance=article)
        count = article.paragraph_set.count()
        self.context['count'] = count
        self.context['form'] = form
        return render(request, self.template_name, self.context)

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
            return redirect('profile-page')
        else:
            self.context['form'] = form
            self.context['count'] = article.paragraph_set.count()
            return render(request, self.template_name, self.context)

    def create_paragraphs(self, request, article, o_count):
        counter = o_count + 1
        for key, value in request.POST.items():
            if key == f"text_area_{counter}":
                paragraph = Paragraph(
                    paragraph=value, article=article, type="1line")
                paragraph.save()
                counter += 1
            if key == f"text_area_split_{counter}":
                paragraph = Paragraph(
                    paragraph=value, article=article, type="split")
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
                paragraph.paragraph = request.POST.get(
                    f"text_area_split_{counter}")
                counter += 1
            paragraph.save()
        return counter


@method_decorator(login_required, name='dispatch')
class ArticleDelete(View):

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return redirect('profile-page')


@method_decorator(login_required, name='dispatch')
class CommentCreate(View):
    data = dict()
    template_name = "blog_site/part/comment_reply_partial.html"

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
            html_content = render_to_string(
                self.template_name, {"comment": comment, 'profile': request.user.profile})
            self.data['successful'] = True
            self.data['html_content'] = html_content
            self.data['pk'] = pk
            return JsonResponse(self.data)
        else:
            self.data['successful'] = False
            html_form = render_to_string(
                self.form_template, {'form': form, 'comment': comment})
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
            self.data['pk'] = pk
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
            html_form = render_to_string(
                self.form_template, {'form': form, 'comment': comment}, request=request)
            self.data['html_form'] = html_form
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
                self.data['pk'] = comment_pk
            except Comment.DoesNotExist:
                self.data['successful'] = False
        else:
            self.data['successful'] = False
            self.data['html_form'] = render_to_string(
                self.form_template, {'form': form})
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
            html_form = render_to_string(
                self.form_template, {'form': form, 'reply': reply}, request=request)
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
                self.data['pk'] = pk
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
            self.data['pk'] = pk
        except Reply.DoesNotExist:
            self.data['successful'] = False
            self.data['message'] = "comment not found"
        return JsonResponse(self.data)


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = "blog_site/user_profile.html"
    form_class = ProfileUpdateForm
    profile_form_class = ProfilePicUpdateForm

    def get(self, request):
        profile = request.user.profile
        articles = Article.objects.filter(author=profile)

        form = ProfileUpdateForm(initial={
            "username": request.user.username,
            "email": request.user.email,
            "job": profile.job,
            "bio": profile.bio,
        })
        profile_pic_form = self.profile_form_class()

        context = {"form": form, "profile_pic_form": profile_pic_form,
                   "profile": profile, "articles": articles}
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        profile = request.user.profile
        articles = Article.objects.filter(author=profile)
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            if form.cleaned_data.get("username"):
                user.username = form.cleaned_data['username']
            if form.cleaned_data.get('job'):
                profile.job = form.cleaned_data['job']
            if form.cleaned_data.get('password'):
                user.set_password(form.cleaned_data['password'])
            if form.cleaned_data.get('bio'):
                user.profile.bio = form.cleaned_data['bio']
            user.save()
            profile.save()
        else:
            context = {"form": form, "profile": profile, "articles": articles}
            return render(request, self.template_name, context)
        return redirect('profile-page')


@method_decorator(login_required, name='dispatch')
class ProfilePicUpdateView(View):
    form_class = ProfilePicUpdateForm

    def post(self, request):
        form = self.form_class(files=request.FILES,
                               instance=request.user.profile)
        if form.is_valid():
            form.save()
        return redirect('profile-page')


class SearchView(View):
    template_name = "blog_site/part/search-article-block.html"
    form_class = SearchForm
    context = dict()  # used to render the template
    data = dict()  # sent to client

    def get(self, request):
        form = self.form_class(request.GET)

        if form.is_valid():
            keyword = form.cleaned_data.get('keyword')
            tag_pattern = r"^(?P<TagSearch>TAG:) *(?P<TagName>[A-Z]+)+$"
            match = re.match(tag_pattern, keyword, re.IGNORECASE)

            if match:
                # extract tag name from regx
                groups = match.groups()
                tag_name = groups[1]
                # search for articles based on tags
                results = Article.objects.filter(tags__name__contains=tag_name)
            else:
                # search for articles based on title
                results = Article.objects.filter(
                    main_title__contains=form.cleaned_data.get('keyword'))

            if results:
                #  add html results
                self.context['articles'] = results
                html_content = render_to_string(
                    self.template_name, self.context, request)

                # add results to data dict
                self.data['success'] = True
                self.data['results_count'] = results.count()
                self.data['html_content'] = html_content
            else:
                # if no results found
                self.data['success'] = False
                self.data['message'] = "no results"
                self.data['results_count'] = 0
        else:
            # if form error occurred
            self.data['success'] = False
            self.data['errors'] = form.errors.as_json()

        return JsonResponse(self.data)
