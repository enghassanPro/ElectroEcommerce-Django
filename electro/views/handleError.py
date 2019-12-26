from django.shortcuts import render
from django.template import RequestContext

# HTTP Error 400
def handler400(request , exception):
    return render(request , "error/400.html" , locals())


def handler403(request , exception):
    return render(request , "error/403.html" , locals())

def handler404(request , exception):
    return render(request , "error/404.html" , locals())

def handler500(request):
    return render(request , "error/500.html" , locals())