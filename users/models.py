from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from .utils import generate_avatar


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields['is_staff'] or not extra_fields['is_superuser']:
            raise ValueError('У суперпользователя должны быть is_staff и is_superuser')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email', unique=True)
    name = models.CharField('Имя', max_length=124)
    surname = models.CharField('Фамилия', max_length=124)
    avatar = models.ImageField('Аватар', upload_to='avatars/')
    # При регистрации телефон не запрашивается, поле может быть пустым
    # Формат и уникальность проверяются в форме редактирования профиля
    phone = models.CharField('Телефон', max_length=12, blank=True)
    github_url = models.URLField('GitHub', blank=True)
    about = models.TextField('О себе', max_length=256, blank=True)
    is_active = models.BooleanField('Активен', default=True)
    is_staff = models.BooleanField('Администратор', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = generate_avatar(self.name)
        super().save(*args, **kwargs)
