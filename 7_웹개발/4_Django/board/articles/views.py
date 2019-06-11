from django.shortcuts import render, redirect
from .models import Article, Comment
from django.utils import timezone
import lipsum
from random import randint

# Create your views here.


# READ
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)


def detail(request, article_id):
    article_selected = Article.objects.get(id=article_id)
    context = {
        'article_selected': article_selected
    }
    return render(request, 'articles/detail.html', context)


# CREATE
# def new(request):
#     return render(request, 'articles/new.html')


def create(request):
    if request.method == 'POST':
        article_new = Article()
        article_new.title = request.POST.get('title')
        article_new.content = request.POST.get('content')
        article_new.save()
        return redirect('articles:detail', article_new.id)
    else:
        return render(request, 'articles/form.html')


# CREATE 10 dummies
def create_dummies(request):
    lip_obj = lipsum.LipsumGen()
    for i in range(10):
        article_dummy = Article()
        article_dummy.title = lip_obj.bytes(randint(1, 10))
        article_dummy.content = lip_obj.paras(randint(1, 10))
        article_dummy.save()
    return redirect('articles:index')


# DELETE
def delete(request, article_id):
    article_selected = Article.objects.get(id=article_id)
    article_selected.delete()
    return redirect('articles:index')


# UPDATE
# def edit(request, article_id):
#     article_selected = Article.objects.get(id=article_id)
#     context = {
#         'article_selected': article_selected,
#     }
#     return render(request, 'articles/edit.html', context)
#

def update(request, article_id):
    article_selected = Article.objects.get(id=article_id)
    if request.method == 'POST':
        article_selected.title = request.POST.get('title')
        article_selected.content = request.POST.get('content')
        article_selected.save()
        return redirect('articles:detail', article_selected.id)
    else:
        context = {
            'article_selected': article_selected,
        }
        return render(request, 'articles/form.html', context)


# CREATE_comment
def create_comment(request, article_id):
    comment_new = Comment()
    comment_new.user = request.META.get('USERNAME')
    comment_new.content = request.POST.get('content')
    comment_new.date = timezone.now()
    comment_new.article = Article.objects.get(id=article_id)
    comment_new.save()
    return redirect('articles:detail', article_id)


# DELETE_comment
def delete_comment(request, article_id, comment_id):
    article_selected = Article.objects.get(id=article_id)
    comment_selected = article_selected.comment_set.get(id=comment_id)
    comment_selected.delete()
    return redirect('articles:detail', article_id)
