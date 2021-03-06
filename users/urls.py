"""users URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path
from django.conf.urls import include, url
from users.views import dashboard, register, datagraph, datagraph_date
from django.urls import path
from . import views
from eyeonwebs.settings import DEBUG, STATIC_URL, STATIC_DIR, MEDIA_DIR, MEDIA_URL,MEDIA_ROOT
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^dashboard/", dashboard, name="dashboard"),
    url(r"^register/", register, name="register"),
    url(r"^datagraph/", datagraph, name="datagraph"),
    url(r"^datagraph_date/", datagraph_date, name="datagraph_date"),
    
 ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

