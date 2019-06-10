from django.shortcuts import render, redirect
from .models import Article

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




