from django.contrib.auth import authenticate , login
from django.shortcuts import render , redirect
from account.forms.user import UserLoginForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages

def view( request ):
    if request.user.is_authenticated:
        return redirect("electro:home")

    elif request.method == "POST":
        return login_submit( request )

    form = UserLoginForm()
    return render(request , "registration/login.html" , {"form":form})

def login_submit( request ):
    check , _ = check_user(request.POST.get('username'))
    json_data = {}
    if check == True:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username , password=password)
            login(request , user)
            if not request.POST.get("remember-me" , None):
                request.session.set_expiry(0)
            json_data['success'] = True
            return JsonResponse(json_data)
        
        if request.is_ajax():
            err_msg = list( form.errors['__all__'].as_data()[0] )[0]
            json_data['form'] = {'password' : err_msg}
            return JsonResponse(json_data)

        else:
            return render(request , "registration/login.html" , { "form": form})

    elif check == False:
        if request.is_ajax():

            json_data['activate'] = request.POST['username']
            return JsonResponse(json_data)
        
        return render( request , "registration/send_activate.html" , {'username':request.POST.get('username')})

    elif check == "error":     
        if request.is_ajax():
            json_data['form'] = {'username':"This User Doesn't Exist.Try again with Correct Username."}
            return JsonResponse(json_data)
        messages.error(request , "This User Doesn't Exist.Register Now to come in our members ^_^")
        return redirect("account:view-login")

    return render(request , "registration/login.html" )

def check_user(username_email):
    try:

        if '@' in username_email:
            user = User.objects.get(email=username_email)
        else:
            user = User.objects.get(username=username_email)
        if not user.is_active:
            return False , None
        return True , user
    except User.DoesNotExist:
        return "error" , None



