from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, telegram_id, password, **extra_fields):
        if not telegram_id:
            raise ValueError("The given telegram_id must be set")
        user = self.model(telegram_id=telegram_id, password=password, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(telegram_id, password, **extra_fields)


class User(AbstractUser):
    telegram_id = models.CharField(_('telegram_id'), max_length=100, unique=True)
    avatar = models.ImageField(verbose_name='avatar', upload_to='users/', **NULLABLE)
    chat_id = models.CharField(max_length=100, **NULLABLE)
    username = None
    email = None

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()