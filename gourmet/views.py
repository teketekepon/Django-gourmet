"""views モジュール。"""
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    """index を実行する。"""
    html = "<h1 style='text-align:center'>グルメ</h1>"
    return HttpResponse(html)
