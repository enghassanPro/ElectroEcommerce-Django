from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text , force_bytes
from account.models.confirm_email import confirm_email
from django.template.loader import render_to_string
from account.token import account_activation_token
from django.db.models import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import redirect 
from django.http import JsonResponse
from django.contrib import messages



class confirmation_email():
    def __init__( self, request , user , template_name ):

        self._request       = request
        self._user          = user
        self._template_name = template_name
        self._uid           = urlsafe_base64_encode(force_bytes(self._user.pk))
        self._token         = account_activation_token.make_token(self._user)
        self._context = {
            'user': self._user , 
            'domain': self._get_current_site(domain=True),
            'uid' : self._uid,
            'token': self._token,
        }
        

    ''' 
        @function to get the current_site 
    '''
    def _get_current_site(self , domain=False):
        '''
            this function can help you for return the host and domain for your current site
            if domain is false then your will get the host and domain otherwise retrive the domain
        '''
        if not domain:
            return get_current_site(self._request)
        
        return get_current_site(self._request).domain

    

    def send_confirmation_email(self , to , from_email=None , subject=None , message=None ):
        
        if message is not None:
            self._context = self._context + message
        messages = render_to_string(self._template_name , self._context)
        email = EmailMessage(subject=subject , body=messages , from_email=from_email , to=to)
        from smtplib import SMTPException
        try:
            email.send()
            store_token = confirm_email(user_id=self._user , token=self._token)
            store_token.save()
            return True
        except SMTPException as e:
            return e

def activate( request , uidb64 , token ):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    
    except (TypeError , ValueError , OverflowError , User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user , token):
        try:
           
            check_token = confirm_email.objects.get(user_id=user , token=token)
            if user.is_active == False:
                if check_token is not None:
                    from django.utils.timezone import now
                    token_created = check_token.created
                    time_now = now()
                    if check_time( token_created , time_now , 10 ):
                        user.is_active = True
                        user.save()
                        check_token.delete()
                        if request.is_ajax():
                            json_data = {}
                            json_data['success'] = 'The Activate Confirmation has been Successfully.\nYou can loging Now!'
                            return JsonResponse(json_data)
                        messages.success(request , "The Activate Confirmation has been Successfully.\nYou can loging Now!")
                        return redirect("account:view-login")

                    else:
                        check_token.delete()
                        if request.is_ajax():
                            json_data = {}
                            json_data['activateError'] = 'This Token was destroied.'
                            return JsonResponse(json_data)
                        
                        messages.error(request  , "This Token was destroied.")
                        return redirect("account:view-login")
                if request.is_ajax():
                    json_data = {}
                    json_data['activateError'] = 'Invalid Token'
                messages.error(request  , "Invalid Token" )
                return redirect("account:view-login")

            else:
                check_token.delete()
                if request.is_ajax():
                    json_data = {}
                    json_data['activateError'] = 'Invalid Token'
                messages.error(request  , "Invalid Token" )
                return redirect("account:view-login")
        except ObjectDoesNotExist:
            if request.is_ajax():
                json_data = {}
                json_data['activateError'] = 'Invalid Token'
            messages.error(request  , "Invalid Token" )
            return redirect("account:view-login")
    else:
        if request.is_ajax():
            json_data = {}
            json_data['activateError'] = 'Invalid Token'
        messages.error(request  , "Invalid Token" )
        return redirect("account:view-login")      

def check_time(datetime_old , datetime_new , timeTaken):
    datetime1 = str(datetime_old)
    datetime2 = str(datetime_new)
    from datetime import datetime , time

    date1 = datetime.strptime(datetime1.split(".")[0].rsplit(":" , 1)[0], '%Y-%m-%d %H:%M')
    date2 = datetime.strptime(datetime2.split(".")[0].rsplit(":" , 1)[0],'%Y-%m-%d %H:%M')
    
    dt = (abs(date2 - date1))
    t = (time(dt.seconds // 3600, (dt.seconds // 60) % 60).strftime('%H:%M'))
    f = t.split(":" , 1 )
    h = f[0]
    m = f[1]
    d = dt.days

    if int(d) > 0 :
        return False
    elif int(h) > 0:
        return False
    elif int(m) > timeTaken:
        return False
    return True

def new_confirmation_email(request , username):

    user = User.objects.get(username=username)
    to_email = [user.email]

    confirmed_mail = confirmation_email(request , user , 'registration/account_activation.html')
    send = confirmed_mail.send_confirmation_email(to_email , subject='Activate Your Account')
    if send == True:
        if request.is_ajax():
            json_data = {}
            json_data['send'] = 'The Activation Code has been sended. check your email!'
            return JsonResponse(json_data)
        messages.success(request , 'The Activation Code has been sended. check your email!')
        return redirect("account:view-login")
    else:
        if request.is_ajax():
            json_data = {}
            json_data['sendError'] = send
            return JsonResponse(json_data)
        messages.error(request , send)
        return redirect('account:view-login')