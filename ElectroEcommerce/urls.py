"""ElectroEcommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url , include
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

handler400 = 'electro.views.handleError.handler400'
handler403 = 'electro.views.handleError.handler403'
handler404 = 'electro.views.handleError.handler404'
handler500 = 'electro.views.handleError.handler500'


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/' , include("account.urls" , namespace="account")),
    url(r'^' , include('electro.urls' , namespace="electro")),
]

SESSION_EXPIRE_AT_BROWSER_CLOSE=True