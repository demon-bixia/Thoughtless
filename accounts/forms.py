from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Profile
User = get_user_model()


class UserCreationForm(forms.ModelForm):

    password = forms.CharField(label="password", max_length=80, widget=forms.PasswordInput(), required=True)
    password_confirm = forms.CharField(label="Confirm password", max_length=80, widget=forms.PasswordInput(), required=True)

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
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'size': '50'}))

    class Meta:
        model = Profile
        fields = ('job', 'profile_pic', 'bio')

    def save(self, commit=True, user=None):
        profile = super(ProfileCreationForm, self).save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return profile


