from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ('username', 'email', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': (('username', 'email',), 'password')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'password_confirm')}),)

    search_fields = ('username', 'email')
    ordering = ('email',)


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
