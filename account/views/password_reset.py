from account.forms.user import PasswordResetForm , ResetNewPasswordForm
from account.views.activate_account import confirmation_email
from account.models.confirm_email import confirm_email
from account.models.old_password import old_password
from django.utils.http import urlsafe_base64_decode 
from account.token import account_activation_token
from django.db.models import ObjectDoesNotExist
from django.shortcuts import render , redirect , HttpResponse
from django.utils.encoding import force_text 
from django.contrib.auth.models import User
from account.views.login import check_user
from django.http import JsonResponse
from django.contrib import messages




def view(request):
    # print(str(request.META['PATH_INFO']).split("/" , 3)[3])
    if request.user.is_authenticated:
        return redirect("electro:home")
    
    elif request.method == 'POST':
        return password_submit(request)
    
    form = PasswordResetForm()
    return render(request , 'registration/password_reset.html' , {'form': form})


def password_submit(request):
    check , user = check_user(request.POST['username_email'])

    if check == True:
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            send_email = confirmation_email(request , user , 'registration/password_reset_msg.html')
            reset_pass = send_email.send_confirmation_email([user.email] , subject="Reset Password")
            if reset_pass == True:

                if request.is_ajax():
                    json_data = {}
                    json_data['msg'] = "An Email has been sent. Please check your inbox email."
                    return JsonResponse(json_data)
                messages.success(request , "An Email has been sent. Please check your inbox email.")
                return redirect("account:view-login")
            
            else:
                if request.is_ajax():
                    json_data = {}
                    json_data['msg'] = reset_pass
                    return JsonResponse(json_data)
                messages.success(request , reset_pass)
                return redirect("account:view-resetPassword")
        if request.is_ajax():
            json_data = {}
            json_data['msg'] = "Enter The correct Username or Email"
            return JsonResponse(json_data)
        messages.success(request , "Enter The correct Username or Email")
        return redirect("account:view-resetPassword")
    elif check == "error":
        if request.is_ajax():
            json_data = {}
            json_data['msg'] = "This User doesn't Exist Try again"
            return JsonResponse(json_data)
        messages.success(request , "This User doesn't Exist Try again")
        return redirect("account:view-resetPassword")


def viewReset( request , uidb64 , token ):


    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    
    except (TypeError , ValueError , OverflowError , User.DoesNotExist):
        user = None

    if request.is_ajax():
        return resetSubmit(request , user)
    else:

        if user is not None and account_activation_token.check_token(user , token):
            try:
                
                check_token = confirm_email.objects.get(user_id=user , token=token)
                form = ResetNewPasswordForm()
                return render(request , "registration/new_password.html" , {"form":form})
            
            except ObjectDoesNotExist:
            
                if request.is_ajax():
                    json_data = {}
                    print("Error")
                    json_data['resetError'] = 'Invalid Token'
                messages.error(request  , "Invalid Token" )
                return redirect("account:view-login")
        if request.is_ajax():
            json_data = {}
            print("Error")
            json_data['activateError'] = 'Invalid Token'
        print("Error")
        messages.error(request  , "Invalid Token" )
        return redirect("account:view-login")      

def resetSubmit(request , user):
    json_data = {}
    form = ResetNewPasswordForm(request.POST)
    if form.is_valid():
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(request , "The password has been reseted You can login Now.")
        return JsonResponse({"success": True })
    json_data['error'] = list( form.errors['__all__'].as_data()[0] )[0]
    return HttpResponse(json_data)
