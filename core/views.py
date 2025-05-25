from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Event, Match, Comment
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from .models import Favorite
from django.contrib import messages

# views.py
def index(request):
    # Берём 5 последних новостей
    all_articles = Article.objects.order_by('-published_at')[:5]
    main_article = all_articles[0] if len(all_articles) > 0 else None
    other_articles = all_articles[1:] if len(all_articles) > 1 else []
    
    events = Event.objects.order_by('date_time')[:5]
    matches = Match.objects.order_by('date_time')[:5]
    
    return render(request, 'index.html', {
        'main_article': main_article,
        'other_articles': other_articles,
        'events': events,
        'matches': matches
    })

def article_detail(request, pk):
    """Детальная страница новости"""
    article = get_object_or_404(Article, pk=pk)
    comments = Comment.objects.filter(article=article).order_by('created_at')
    return render(request, 'article_detail.html', {'article': article, 'comments': comments})

def event_detail(request, pk):
    """Детальная страница события"""
    event = get_object_or_404(Event, pk=pk)
    comments = Comment.objects.filter(event=event).order_by('created_at')
    return render(request, 'event_detail.html', {'event': event, 'comments': comments})

def match_detail(request, pk):
    match = get_object_or_404(Match, pk=pk)
    comments = Comment.objects.filter(match=match).order_by('created_at')
    
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(
                user=request.user,
                match=match,
                content=content
            )
            return redirect('match_detail', pk=pk)
    
    return render(request, 'match_detail.html', {
        'match': match,
        'comments': comments
    })

# views.py
def all_matches(request):
    matches = Match.objects.order_by('-date_time')
    return render(request, 'all_matches.html', {'matches': matches})

def auth_view(request):
    """Отдельная страница для авторизации/регистрации"""
    if request.user.is_authenticated:
        return redirect('index')
    
    login_form = LoginForm(request=request)
    register_form = RegisterForm()
    
    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = LoginForm(request=request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('index')
        
        elif 'register_submit' in request.POST:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('index')
    
    return render(request, 'auth.html', {
        'login_form': login_form,
        'register_form': register_form
    })

def logout_view(request):
    """Выход из системы"""
    logout(request)
    return redirect('index')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    favorite_articles = Favorite.objects.filter(user=request.user, article__isnull=False).select_related('article')
    favorite_events = Favorite.objects.filter(user=request.user, event__isnull=False).select_related('event')
    
    return render(request, 'profile.html', {
        'user': request.user,
        'favorite_articles': favorite_articles,
        'favorite_events': favorite_events
    })


def add_event_to_favorites(request, event_id):
    if not request.user.is_authenticated:
        return redirect('auth')
    
    event = get_object_or_404(Event, id=event_id)
    
    fav, created = Favorite.objects.get_or_create(
        user=request.user,
        event=event
    )
    
    if created:
        messages.success(request, "Событие добавлено в избранное")
    else:
        messages.info(request, "Событие уже в избранном")
    
    return redirect('index')

def add_article_to_favorites(request, article_id):
    if not request.user.is_authenticated:
        return redirect('auth')
    
    article = get_object_or_404(Article, pk=article_id)
    
    existing = Favorite.objects.filter(user=request.user, article=article).first()
    if not existing:
        Favorite.objects.create(user=request.user, article=article)
        messages.success(request, "Новость добавлена в избранное.")
    else:
        messages.info(request, "Новость уже в избранном.")
    
    return redirect('index')