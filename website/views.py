from django.shortcuts import render


# 返回index.html页面
def index(request):
    return render(request, "index.html")
