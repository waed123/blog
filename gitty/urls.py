from django.conf.urls import url, include
from . import views

urlpatterns = [  
	url(r'^members/$', views.member_list , name="members"),
	
]