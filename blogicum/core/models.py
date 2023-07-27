from django.db import models


class PublishedModel(models.Model):

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        null=False,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    created_at = models.DateTimeField(
        auto_now_add=True, null=False,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True
