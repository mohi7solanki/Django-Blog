from django.shortcuts import render, get_object_or_404
from urllib.parse import quote
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from django.db.models import Q
from .forms import PostForm
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone


def post_list(request):
    if not request.user.is_authenticated:
        all_posts = Post.objects.active()
    else:
        all_posts = Post.objects.all()
    query = request.GET.get('q')
    error_msg = ''
    if query:
        all_posts = all_posts.filter(
            Q(title__icontains = query)|
            Q(content__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
            ).distinct()
        if len(all_posts) < 1:
            error_msg = "Sorry No Posts available for given query!"
    paginator = Paginator(all_posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'error_msg': error_msg,
    }
    return render(request, 'posts/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.draft or post.publish > timezone.now().date():
        if not request.user.is_authenticated:
            raise Http404
    share_string = quote(post.content)
    context = {
        'post':post,
        'share_string':share_string,
    }
    return render(request, 'posts/detail.html', context)


def post_create(request):
    if not request.user.is_authenticated:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Post added succesfully!')
        return HttpResponseRedirect(reverse('posts:index'))
    context = {
        'form': form,
    }
    return render(request, 'posts/form.html', context)


def post_update(request, slug):
    if not request.user.is_authenticated:
        raise Http404
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, 'Changes Saved!')
        return HttpResponseRedirect(reverse('posts:detail', args=(slug,)))
    context = {
        'form':form,
    }
    return render(request, 'posts/form.html', context)


def post_delete(request, slug):
    if not request.user.is_authenticated:
        raise Http404
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Successfully deleted!')
        return HttpResponseRedirect(reverse('posts:index'))
    context = {
        'post': post,
    }
    return render(request, 'posts/confirm_delete.html', context)



