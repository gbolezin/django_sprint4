from django.db import models
from django.contrib.auth import get_user_model

from core.models import PublishedModel


User = get_user_model()


class Category(PublishedModel):
    title = models.CharField(
        max_length=256, verbose_name='Заголовок', null=False
    )
    description = models.TextField(
        verbose_name='Описание',
        null=False
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name='Идентификатор',
        null=False,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, '
            'дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(
        max_length=256,
        verbose_name='Название места',
        null=False
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
        null=False,
        blank=False
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    slug = models.SlugField(
        max_length=64,
        verbose_name='Идентификатор',
        null=False,
        blank=False,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, '
            'дефис и подчёркивание.'
        )
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        auto_now=False,
        help_text=(
            'Если установить дату и время в будущем '
            '— можно делать отложенные публикации.'
        )
    )

    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
        related_name='posts',
        null=False,
        blank=False
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Местоположение',
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Категория',
        null=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
