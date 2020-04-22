"""Модуль для работы с БД через ORM."""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """Определеяет таблицу mainpage_task в БД через ORM."""

    title_length = 200
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    executor = models.ManyToManyField('Profile', blank=True)
    title = models.CharField(max_length=title_length)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """Определяет поведение функции str(), вызванной для экземпляра класса.

        Returns:
            title(str): Заголовок экземпляра класса.
        """
        return self.title

    class Meta(object):
        """Класс для метаданных.

        Когда Django конструирует класс Task, Meta переопределяет verbose_name
        и verbose_name_plural, чтобы в админке отображать эти имена корректно.
        """

        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Profile(models.Model):
    """Определеяет таблицу mainpage_profile в БД через ORM."""

    max_length = 100
    email_max_length = 150
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=max_length, blank=True)
    last_name = models.CharField(max_length=max_length, blank=True)
    email = models.EmailField(max_length=email_max_length, blank=True)

    def __str__(self):
        """Определяет поведение функции str(), вызванной для экземпляра класса.

        Returns:
            user.username(str): Имя пользователя из таблицы user.
        """
        return self.user.username
