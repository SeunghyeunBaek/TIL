from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post


def index(request):
    # posts = Post.objects.order_by('-id')
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'posts/index.html', context)


def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)   # 데이터와 이미지 모두 저장
        if form.is_valid():
            form.save()
            return redirect('posts:index')
        else:
            pass  # form 이 유효하지 않으면 save 하지 않고 기존 form 을 넘긴다.
    else:
        form = PostForm()  # GET 이면 새로운 FORM 을 만든다.
    context = {
        'form': form
    }
    return render(request, 'posts/form.html', context)


def update(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:index')
        else:
            pass
    else:
        form = PostForm(instance=post)
        context = {
            'form': form,
        }
    return render(request, 'posts/form.html', context)


def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('posts:index')

# def create(request):
#     # 1. if request.method is GET, request Form
#     # 4. if request.method is POST,
#     # 9. user writes valid data
#     if request.method == 'POST':
#         # 5. create PostForm instance with input data(request.POST)
#         # 10. create PostForm instance with input data(request.POST)
#         form = PostForm(request.POST)
#         # 6. validate input data
#         # 11. validate input data
#         if form.is_valid():
#             # if form is valid, save data and redirect to posts/
#             form.save()
#             return redirect('post:index')
#         else:
#             # 7 if form is not valid, go outer else
#             pass
#     else:
#         form = PostForm()
#         # 2. create instance of PostForm
#     context = {
#         'form': form
#     }
#     # 3. render posts/create.html with PostForm and send it to posts/create
#     # 8. send form with valid data
#     return render(request, 'posts/create.html', context)





