from django.shortcuts import render, redirect
from .models import Article, Comment
from django.utils import timezone


def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)


def detail(request, article_id):
    article_selected = Article.objects.get(id=article_id)
    context = {
        'article_selected': article_selected,
    }
    return render(request, 'articles/detail.html', context)


def create(request):
    if request.method == 'POST':
        article_new = Article()
        article_new.title = request.POST.get('title')
        article_new.content = request.POST.get('content')
        article_new.user = request.user
        article_new.date = timezone.now()
        article_new.save()
        return redirect('articles:detail', article_new.id)
    else:
        return render(request, 'articles/form.html')


def update(request, article_id):
    article_selected = Article.objects.get(id=article_id)
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
    article_selected = Article.objects.get(id=article_id)
    article_selected.delete()
    return redirect('articles:index')


def create_comment(request, article_id):
    comment_new = Comment()
    comment_new.user = request.user
    comment_new.content = request.POST.get('content')
    comment_new.date = timezone.now()
    comment_new.article_id = article_id
    comment_new.save()
    return redirect('articles:detail', article_id)


def delete_comment(request, article_id, comment_id):
    comment_selected = Comment.objects.get(id=comment_id)
    comment_selected.delete()
    return redirect('articles:detail', article_id)

