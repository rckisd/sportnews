from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Article, Event, Comment, Favorite

class CommentInlineArticle(admin.TabularInline):
    model = Comment
    fk_name = 'article'
    extra = 1

class CommentInlineEvent(admin.TabularInline):
    model = Comment
    fk_name = 'event'
    extra = 1

class FavoriteInlineArticle(admin.TabularInline):
    model = Favorite
    fk_name = 'article'
    extra = 1

class FavoriteInlineEvent(admin.TabularInline):
    model = Favorite
    fk_name = 'event'
    extra = 1

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'created_at')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('id',)
    readonly_fields = ('created_at',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительные поля', {
            'fields': ('role', 'created_at'),
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Дополнительные поля', {
            'fields': ('role',),
        }),
    )
    verbose_name = 'Пользователь'
    verbose_name_plural = 'Пользователи'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Админка для новостей (Article)"""
    list_display = ('title', 'author', 'published_at', 'comment_count')
    list_display_links = ('title',)
    list_filter = ('author',)
    date_hierarchy = 'published_at'
    search_fields = ('title', 'content')
    raw_id_fields = ('author',)
    readonly_fields = ('published_at',)
    inlines = [CommentInlineArticle, FavoriteInlineArticle]

    def comment_count(self, obj):
        return obj.comment_set.count()
    comment_count.short_description = 'Количество комментариев'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Админка для событий (Event)"""
    list_display = ('title', 'date_time', 'location', 'status', 'comment_count')
    list_filter = ('status', 'location')
    date_hierarchy = 'date_time'
    search_fields = ('title', 'description', 'location')
    raw_id_fields = ()
    inlines = [CommentInlineEvent, FavoriteInlineEvent]

    def comment_count(self, obj):
        return obj.comment_set.count()
    comment_count.short_description = 'Количество комментариев'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка для комментариев"""
    list_display = ('user', 'article', 'event', 'created_at')
    list_filter = ('created_at', 'user')
    date_hierarchy = 'created_at'
    search_fields = ('content', 'user__username')
    raw_id_fields = ('user', 'article', 'event')
    readonly_fields = ('created_at',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Админка для избранного"""
    list_display = ('user', 'article', 'event', 'added_at')
    list_filter = ('added_at', 'user')
    date_hierarchy = 'added_at'
    search_fields = ('user__username',)
    raw_id_fields = ('user', 'article', 'event')
    readonly_fields = ('added_at',)

