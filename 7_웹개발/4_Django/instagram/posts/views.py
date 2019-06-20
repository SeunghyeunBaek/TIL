from django.contrib.auth.decorators import login_required  # 로그인 관련 기능
from django.shortcuts import render, redirect
from .models import Post, Comment, HashTag
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from itertools import chain


def all(request):
    # posts = Post.objects.order_by('-id')
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/index.html', context)


@login_required
def index(request):
    # posts = Post.objects.order_by('-id')
    # 내가 팔로우 한 사람의 글만 피드
    user_login = request.user
    user_follow = user_login.follow.all()
    follow_list = chain(user_follow, [request.user])  # user_follow + user
    posts = Post.objects.filter(user__in=follow_list)  # user 가 팔로우 하는 사람만 출력
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/index.html', context)


@login_required  # 로그인 상태에서만 동작
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # 데이터(POSTS)와 이미지(FILES) 모두 저장
        # 데이터 검증, 불필요한 데이터 정리(스트링 앞뒤에 붙어 있는 빈공간 등등)
        if form.is_valid():
            # user 정보를 넣고 save
            post = form.save(commit=False)  # post object(None)
            post.user = request.user
            post.save()
            # 해시태그 추가
            # post_id, hash_tag_id 가 부여돼야(저장돼야) 둘을 연결할 수 있다.
            content = form.cleaned_data.get('content')  # strip 기능
            words = content.split()
            for word in words:
                if word[0] == '#':
                    hash_tag_new = HashTag.objects.get_or_create(content=word)  # 이미 있으면 get, 없으면 create
                    post.hash_tags.add(hash_tag_new[0])  # post 와 연결
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
                # 해시태그 업데이트
                post.hash_tags.clear()  # 기존의 해시태그 관계를 다 끊는다.
                content = form.cleaned_data.get('content')  # strip 기능
                words = content.split()
                for word in words:
                    if word[0] == '#':
                        hash_tag_new = HashTag.objects.get_or_create(content=word)  # 이미 있으면 get, 없으면 create
                        post.hash_tags.add(hash_tag_new[0])  # post 와 연결
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


@login_required
def comment_delete(request, post_id, comment_id):
    comment_selected = Comment.objects.get(id=comment_id)
    if request.user == comment_selected.user:
        comment_selected.delete()
    return redirect('posts:index')


@login_required
def comment_update(request, post_id, comment_id):
    comment_selected = Comment(id=comment_id)
    if request.method == 'POST':
        pass
    else:
        comment_form = CommentForm(data=request.POST, instance=comment_selected)
    context = {
        'form': comment_form,
    }
    return render(request, 'posts:index')


@login_required
def likes(request, post_id):
    user = request.user  # 좋아요을 누른 사용자
    post = Post.objects.get(id=post_id)  # 좋아한 게시물

    if user in post.like_users.all():
        # 이미 좋아요가 눌린 게시물일 경우 => 좋아요 취소
        post.like_users.remove(user)
        is_like = False
    else:
        # 좋아요를 누르지 않은 경우 => 좋아요 추가
        post.like_users.add(user)
        is_like = True
    # return redirect('posts:index')
    # javascript 로 변수 전달
    like_count = post.like_users.count()
    context = {
        'is_like': is_like,
        'like_count': like_count,
    }
    return JsonResponse(context)


# 선택된 hash_tag 를 포함한 모든 post 출력
def hash_tags(request, hash_tag_id):
    hash_tag_selected = HashTag.objects.get(id=hash_tag_id)
    posts_hash_tagged = hash_tag_selected.post_tagged.all()
    comment_form = CommentForm()
    context = {
        'posts': posts_hash_tagged,
        'comment_form': comment_form,
        'hash_tag': hash_tag_selected,
    }
    return render(request, 'posts/index.html', context)


def javascript(request):
    return render(request, 'posts/javascript.html')
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
