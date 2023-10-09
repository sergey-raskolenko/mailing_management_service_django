from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import UserManager as UserBaseManager, AbstractUser

NULLABLE = {'blank': True, 'null': True}


class UserManager(UserBaseManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    first_name = models.CharField(max_length=150, verbose_name='имя',**NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='фото', **NULLABLE)
    token = models.CharField(max_length=200, verbose_name='токен верификации', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
