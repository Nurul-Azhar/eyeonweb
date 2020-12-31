from django.conf.urls import url 
from django.urls import path
from . import views
from eyeonwebs.settings import DEBUG, STATIC_URL, STATIC_DIR, MEDIA_DIR, MEDIA_URL

urlpatterns = [
    path('', views.index, name='index'),
    path('datagraph/',views.datagraph, name='datagraph'),
]