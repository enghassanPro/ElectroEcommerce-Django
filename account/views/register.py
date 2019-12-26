from django.contrib.auth import authenticate , login
from .activate_account import confirmation_email
from account.forms.user import UserRegisterForm
from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages


def view( request ):
    if request.user.is_authenticated:
        return redirect("electro:home")
    
    if request.method == "POST":
        return register_submit(request)
        
    form = UserRegisterForm()
    return render(request , "registration/register.html" , {"form":form})


def register_submit(request):

    form = UserRegisterForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        to_mail = [ form.cleaned_data['email'] ]
        confirmed_email = confirmation_email(request , user , 'registration/account_activation.html')
        send = confirmed_email.send_confirmation_email(to_mail , subject='Activate Your Account')
        if send == True:
            messages.success(request , 'registration Successfully and Activation has been sended.')
            return redirect("account:view-login")
        else:
            messages.error(request , send)
            return redirect('account:view-register')

        

    return render(request , "registration/register.html" , {"form":form})
 


