from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCreationForm, ProfileCreationForm
from django.views.generic import View
from django.contrib.auth import views as built_in_views
from django.contrib.auth import logout, get_user_model
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy

User = get_user_model()


# noinspection PyMethodMayBeStatic
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
            messages.success(request, "we've sent a confirmation email to you address")
            return redirect('login-view')
        else:
            return render(request, self.template_name, self.context)

    def form_valid(self, request):
        user = self.context['form'].save(commit=False)
        user.is_active = False
        user.save()
        self.send_activation_token(request, user, user.email)
        self.context['p_form'].save(user=user)

    def send_activation_token(self, request, user, email):
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        message = render_to_string('accounts/account_activation_template.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        to_email = email
        email = EmailMessage(
            mail_subject,
            message,
            to=[to_email]
        )
        email.send()


class ActivateAccount(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'your account is activated now you can login')
            return redirect('login-view')
        else:
            return HttpResponse("activation link invalid")


class LoginView(built_in_views.LoginView):
    template_name = 'accounts/login.html'


# noinspection PyMethodMayBeStatic
@method_decorator(login_required, name='dispatch')
class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('login-view')


class PasswordResetView(built_in_views.PasswordResetView):
    template_name = "accounts/password_reset/password_reset.html"
    subject_template_name = "accounts/password_reset/subject.text"
    email_template_name = "accounts/password_reset/password_reset_email.html"
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDoneView(built_in_views.PasswordResetDoneView):
    template_name = "accounts/password_reset/password_reset_done.html"


class PasswordResetConfirmView(built_in_views.PasswordResetConfirmView):
    template_name = "accounts/password_reset/password_reset_confirm.html"
    success_url = reverse_lazy('password_reset_complete')


class PasswordResetCompleteView(built_in_views.PasswordResetCompleteView):
    template_name = "accounts/password_reset/password_reset_complete.html"


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
