from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, username, email, date_joined, password=None):
        if not email:
            raise ValueError("email field is required")
        if not username:
            raise ValueError("username field is required")
        user = self.model(username=username, email=email, date_joined=date_joined)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, date_joined, password):
        user = self.create_user(username=username, email=email, date_joined=date_joined, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=60)
    email = models.EmailField(max_length=255, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['date_joined', 'username']
    objects = UserManager()

    def ___str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser


def save_profile_pic(instance, filename):
    return f"{instance.user.pk}/profile_pics/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_pic = models.ImageField(upload_to=save_profile_pic, default="/default/default.png", blank=True)
    job = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.user.username
