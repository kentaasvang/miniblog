from django.shortcuts import render
from django.http import (
    HttpRequest,
    HttpResponse
    )
from .models import Post


def index(req):
    posts = Post.objects.filter(is_published=True)
    context = {"posts": posts}
    return render(req, "gui/index.html", context=context)


def post(req, id):
    post = Post.objects.get(id=id) 
    context = {"post": post}
    return render(req, "gui/post.html", context=context)
