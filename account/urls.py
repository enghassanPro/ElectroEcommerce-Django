from django.conf.urls import url , include
from django.contrib.auth import settings
from django.conf.urls.static import static
from .views import login , logout , register , activate_account , password_reset

# register namespace
app_name= 'account'

urlpatterns = [

    url(r'^auth/login/$' , login.view , name="view-login"),
    url(r'^auth/register/$' , register.view , name='view-register'),
    url(r'^auth/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$' , 
        activate_account.activate , name='activate'),
    url(r'^auth/activate/confirmed_mail(?:username=(?P<username>[0-9A-Za-z]+))' , activate_account.new_confirmation_email , name='new-confirm-mail'),
    url(r'^auth/logout$' , logout.view , name='logout'),
    url(r'^auth/reset-password/$', password_reset.view , name='view-resetPassword'),
    url(r'^auth/reset-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$' , 
    password_reset.viewReset , name='view-reset'),
    url(r'^oauth/' , include('social_django.urls' , namespace='social'))

] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)