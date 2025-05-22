from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth_view, name='auth'),  # Отдельная страница для авторизации
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('favorite/article/<int:article_id>/', views.add_article_to_favorites, name='add_article_to_favorites'),
    path('favorite/event/<int:event_id>/', views.add_event_to_favorites, name='add_event_to_favorites'),

]