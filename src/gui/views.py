from django.shortcuts import render
from django.http import (
    HttpRequest,
    HttpResponse
    )


def index(req: HttpRequest) -> HttpResponse:
    return render(req, "gui/index.html")
