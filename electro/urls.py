from django.conf.urls import url
from django.contrib.auth import settings
from django.conf.urls.static import static
from .views import index

# register namespace
app_name= 'electro'

urlpatterns = [

    url(r'^$' , index.index , name='home'),

] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)