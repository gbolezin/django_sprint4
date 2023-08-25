from django.db import models
from django.contrib.auth import get_user_model

from core.models import PublishedModel

MAX_LENGTH_256 = 256
MAX_LENGTH_64 = 64
MAX_LENGTH_STR_TITLE = 10
MAX_LENGTH_STR_TEXT = 20
User = get_user_model()


class Category(PublishedModel):
    title = models.CharField(
        max_length=MAX_LENGTH_256,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_64,
        unique=True,
        verbose_name='Идентификатор',
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
        return self.title[:MAX_LENGTH_STR_TITLE]


class Location(PublishedModel):
    name = models.CharField(
        max_length=MAX_LENGTH_256,
        verbose_name='Название места',
        null=False
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:MAX_LENGTH_STR_TITLE]


class Post(PublishedModel):
    title = models.CharField(
        max_length=MAX_LENGTH_256,
        verbose_name='Заголовок',
        blank=False
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_64,
        verbose_name='Идентификатор',
        blank=False,
        default='default',
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

    image = models.ImageField('Фото', upload_to='post_images', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:MAX_LENGTH_STR_TITLE]


class Comment(PublishedModel):
    text = models.TextField(
        verbose_name='Текст'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата и время публикации',
        auto_now=True,
        blank=False
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        related_name='comments',
        verbose_name='Пост',
        null=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return self.text[:MAX_LENGTH_STR_TEXT]
