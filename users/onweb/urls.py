from django.conf.urls import url 
from django.urls import path
from . import views
from eyeonwebs.settings import DEBUG, STATIC_URL, STATIC_DIR, MEDIA_DIR, MEDIA_URL

urlpatterns = [
    path('', views.index, name='index'),
    path('datascrap/',views.datagraph, name='datascrap'),
    # path('datagraph/',views.datagraph, name='datagraph'),
    # path('<str:filepath>/', views.download_file,name = 'download_file')
]