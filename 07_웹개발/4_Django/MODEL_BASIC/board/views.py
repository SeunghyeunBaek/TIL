from django.shortcuts import render, redirect
from .models import Article


# Create Article
def article_create(request):
    return render(request, 'board/article_create.html')


# Save Article
def article_save(request):
    if request.method == 'POST':
        article_new = Article()
        article_new.title = request.POST.get('title')
        article_new.content = request.POST.get('content')
        article_new.save()
        return redirect(f'/board/{article_new.id}')
    else: return redirect(f'/board/')


# Read all
def article_list(request):  # 전체 article 조회하기
    articles = Article.objects.all()  # get all list of article objects
    context = {
        'articles': articles,
    }
    return render(request, 'board/article_list.html', context)


# Read one
def article_detail(request, article_id):  # 특정 article 조회하기
    article_selected = Article.objects.get(id=article_id)
    context = {
        'article_selected': article_selected,
    }
    return render(request, 'board/article_detail.html', context)


# Update
def article_edit(request, article_id):
    article_selected = Article.objects.get(id=article_id)
    context = {
        'article_selected': article_selected,
    }
    return render(request, 'board/article_edit.html', context)


def article_update(request, article_id):
    if request.method == 'POST':
        article_selected = Article.objects.get(id=article_id)
        article_selected.title = request.POST.get('title')
        article_selected.content = request.POST.get('content')
        article_selected.save()
        return redirect(f'/board/{article_selected.id}/')
    else: return redirect(f'/board/{article_id}')


# Delete
def article_delete(request, article_id):
    article_selected = Article.objects.get(id=article_id)
    article_selected.delete()
    return redirect('/board/')

