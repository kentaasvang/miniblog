from django.shortcuts import render
from django.http import (
    HttpRequest,
    HttpResponse
    )
from .models import Post


def index(req: HttpRequest) -> HttpResponse:
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(req, "gui/index.html", context=context)
