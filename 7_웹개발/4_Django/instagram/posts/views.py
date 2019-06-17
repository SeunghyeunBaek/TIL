from django.contrib.auth.decorators import login_required  # 로그인 관련 기능
from django.shortcuts import render, redirect
from .forms import PostForm, CommentForm
from .models import Post


def index(request):
    # posts = Post.objects.order_by('-id')
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/index.html', context)


@login_required  # 로그인 상태에서만 동작
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)   # 데이터(POSTS)와 이미지(FILES) 모두 저장
        if form.is_valid():
            # user 정보를 넣고 save
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
        else:
            pass  # form 이 유효하지 않으면 save 하지 않고 기존 form 을 넘긴다.
    else:
        form = PostForm()  # GET 이면 새로운 FORM 을 만든다.
    context = {
        'form': form
    }
    return render(request, 'posts/form.html', context)


@login_required
def update(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.user:
        # 내가 작성한 글일때
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
    else:
        # 내가 작성하지 않은 글일 때
        return redirect('posts:index')


def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.user:
        post.delete()
        return redirect('posts:index')
    else:
        return redirect('posts:index')


@login_required
def comment_create(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_new = comment_form.save(commit=False)
            comment_new.user = request.user
            comment_new.post = post
            # comment_new.post_id = post_id
            # foreign key 는 model_id 변수를 만든다.
            comment_new.save()
            return redirect('posts:index')


def comment_update(request, post_id, comment_id):
    pass


def comment_delete(request, post_id, comment_id):
    pass


@login_required
def likes(request, post_id):
    user = request.user  # 좋아요을 누른 사용자
    post = Post.objects.get(id=post_id)  # 좋아한 게시물
    if user in post.like_users.all():
        # 이미 좋아요가 눌린 게시물일 경우 => 좋아요 취소
        post.like_users.remove(user)
    else:
        # 좋아요를 누르지 않은 경우 => 좋아요 추가
        post.like_users.add(user)
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





