from django.shortcuts import render, redirect
from .models import Articles
from django.utils import timezone


def index(request):
    articles = Articles.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)


def detail(request, article_id):
    article_selected = Articles.objects.get(id=article_id)
    context = {
        'article_selected': article_selected,
    }
    return render(request, 'articles/detail.html', context)


def create(request):
    if request.method == 'POST':
        article_new = Articles()
        article_new.title = request.POST.get('title')
        article_new.content = request.POST.get('content')
        article_new.user = request.META.get('USERNAME')
        article_new.date = timezone.now()
        article_new.save()
        return redirect('articles:detail', article_new.id)
    else:
        return render(request, 'articles/form.html')


def update(request, article_id):
    article_selected = Articles.objects.get(id=article_id)
    if request.method == 'POST':
        article_selected.title = request.POST.get('title')
        article_selected.content = request.POST.get('content')
        article_selected.date = timezone.now()
        article_selected.save()
        return redirect('articles:detail', article_selected.id)
    else:
        context = {
            'article_selected': article_selected,
        }
        return render(request, 'articles/form.html', context)


def delete(request, article_id):
    article_selected = Articles.objects.get(id=article_id)
    article_selected.delete()
    return redirect('articles:index')
