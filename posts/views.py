from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import PostForm
from django.urls import reverse
from django.contrib import messages


def post_list(request):
    all_posts = Post.objects.order_by('-timestamp')
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
    }
    return render(request, 'posts/post_list.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post':post,
    }
    return render(request, 'posts/detail.html', context)


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Post added succesfully!')
        return HttpResponseRedirect(reverse('posts:index'))
    context = {
        'form':form,
    }
    return render(request, 'posts/form.html', context)


def post_update(request, slug):
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
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, 'Successfully deleted!')
    return HttpResponseRedirect(reverse('posts:index'))



