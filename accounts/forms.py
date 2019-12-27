from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Profile

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label="password", max_length=80, widget=forms.PasswordInput(), required=True)
    password_confirm = forms.CharField(label="Confirm password", max_length=80, widget=forms.PasswordInput(),
                                       required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password_confirm(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password_confirm']

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("passwords mismatch")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        return self.initial['password']


class ProfileCreationForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, label="fullscreen")
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'size': '50'}), required=False)

    class Meta:
        model = Profile
        fields = ('job', 'profile_pic', 'bio')

    def save(self, commit=True, user=None):
        profile = super(ProfileCreationForm, self).save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return profile


class ProfileUpdateForm(forms.Form):
    username = forms.CharField(label="username", max_length=80, min_length=3, required=False)
    job = forms.CharField(label="job", max_length=50, min_length=3, required=False)
    password = forms.CharField(label="password", max_length=80, min_length=8,
                               widget=forms.PasswordInput(render_value=True), required=False)
    password_confirm = forms.CharField(label="password confirm", max_length=80, min_length=8,
                                       widget=forms.PasswordInput(render_value=True),
                                       required=False)
    bio = forms.CharField(label="bio", widget=forms.Textarea(), required=False)

    def clean(self):
        cleaned_data = super(ProfileUpdateForm, self).clean()

        if cleaned_data.get("password") and not cleaned_data.get("password_confirm"):
            raise forms.ValidationError("Password is not confirmed")

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("password mismatch")

        return password_confirm


class ProfilePicUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("profile_pic",)
