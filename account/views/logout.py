from django.shortcuts import render , redirect
from django.contrib.auth import logout


def view(request):
    logout(request)
    return redirect("account:view-login")