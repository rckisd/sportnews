from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Пользователь (на базе AbstractUser)"""
    ROLES = (
        ('guest', 'Guest'),
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Article(models.Model):
    """Новость"""
    title = models.CharField('Заголовок', max_length=255)
    content = models.TextField('Содержание')
    published_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, verbose_name='Автор', on_delete=models.CASCADE, related_name='articles'
    )
    image_url = models.CharField('URL изображения', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'articles'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

class Event(models.Model):
    """Событие (мероприятие)"""
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('finished', 'Finished'),
    )
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True, null=True)
    date_time = models.DateTimeField('Дата и время')
    location = models.CharField('Место', max_length=255, blank=True, null=True)
    status = models.CharField(
        'Статус', max_length=10, choices=STATUS_CHOICES, default='upcoming'
    )

    class Meta:
        db_table = 'events'
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return self.title

class Match(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Предстоящий'),
        ('live', 'В прямом эфире'),
        ('finished', 'Завершенный'),
    )
    team_a = models.CharField('Команда A', max_length=100)
    team_b = models.CharField('Команда B', max_length=100)
    score_a = models.PositiveSmallIntegerField('Счёт команды A', default=0)
    score_b = models.PositiveSmallIntegerField('Счёт команды B', default=0)
    date_time = models.DateTimeField('Дата и время матча')
    status = models.CharField(
        'Статус', max_length=10, choices=STATUS_CHOICES, default='upcoming'
    )
    tournament = models.CharField('Турнир', max_length=200, blank=True)
    location = models.CharField('Место проведения', max_length=200, blank=True)

    class Meta:
        db_table = 'matches'
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'
        ordering = ['date_time']
    
    def __str__(self):
        return f"{self.team_a} vs {self.team_b}"


class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, verbose_name='Новость', on_delete=models.CASCADE, null=True, blank=True
    )
    event = models.ForeignKey(
        Event, verbose_name='Событие', on_delete=models.CASCADE, null=True, blank=True
    )
    match = models.ForeignKey(  # Добавляем новое поле
        'Match', verbose_name='Матч', on_delete=models.CASCADE, null=True, blank=True
    )
    content = models.TextField('Содержание')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(article__isnull=False, event__isnull=True, match__isnull=True) |
                    models.Q(article__isnull=True, event__isnull=False, match__isnull=True) |
                    models.Q(article__isnull=True, event__isnull=True, match__isnull=False)
                ),
                name='check_comment_target'
            )
        ]

    def __str__(self):
        target = self.article if self.article else self.event
        return f'Комментарий {self.user.username} к {target}'

class Favorite(models.Model):
    """Избранное (связка пользователь-новость или пользователь-событие)"""
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, verbose_name='Новость', on_delete=models.CASCADE, null=True, blank=True
    )
    event = models.ForeignKey(
        Event, verbose_name='Событие', on_delete=models.CASCADE, null=True, blank=True
    )
    added_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    
    class Meta:
        db_table = 'favorites'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(article__isnull=False, event__isnull=True) |
                    models.Q(article__isnull=True, event__isnull=False)
                ),
                name='check_favorite_article_or_event'
            ),
            models.UniqueConstraint(fields=['user', 'article'], name='unique_user_article'),
            models.UniqueConstraint(fields=['user', 'event'], name='unique_user_event'),
        ]

    def __str__(self):
        target = self.article if self.article else self.event
        return f'Избранное {self.user.username}: {target}'