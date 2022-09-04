from django.shortcuts import render
from django.http import (
    HttpRequest,
    HttpResponse,
    Http404
    )

from .models import Post


def index(req):
    posts = Post.objects.filter(is_published=True)
    context = {"posts": posts}
    return render(req, "gui/index.html", context=context)


def post(req, id):

    try:
        post = Post.objects.get(id=id, is_published=True) 
    except Post.DoesNotExist:
        raise Http404("post does not exist")
    
    context = {"post": post}
    return render(req, "gui/post.html", context=context)
