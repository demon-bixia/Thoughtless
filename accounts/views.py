from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth import views as built_in_views
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View

from .forms import UserCreationForm, ProfileCreationForm

User = get_user_model()


class RegisterView(View):
    template_name = "accounts/register.html"
    form_class = UserCreationForm
    profile_form_class = ProfileCreationForm
    context = {}

    def get(self, request):
        form = self.form_class()
        p_form = self.profile_form_class()
        self.context['form'] = form
        self.context['p_form'] = p_form
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = self.form_class(request.POST)
        p_form = self.profile_form_class(request.POST, request.FILES)
        self.context['form'] = form
        self.context['p_form'] = p_form
        if form.is_valid() and p_form.is_valid():
            self.form_valid(request)
            return redirect('login-view')
        else:
            return render(request, self.template_name, self.context)

    def form_valid(self, request):
        user = self.context['form'].save(commit=True)
        self.context['p_form'].save(user=user)


class LoginView(built_in_views.LoginView):
    template_name = 'accounts/login.html'


@method_decorator(login_required, name='dispatch')
class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('login-view')


class AjaxRegister(View):
    data = {}

    def get(self, request):
        email = request.GET.get('email')
        self.email_valid(email)
        return JsonResponse(self.data)

    def email_valid(self, email):
        try:
            user = User.objects.get(email=email)
            if user:
                self.data['is_valid'] = False
        except User.DoesNotExist:
            self.data['is_valid'] = True
        return self.data
