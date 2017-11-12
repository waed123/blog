from django.conf.urls import url, include
from . import views

urlpatterns = [  
    url(r'^list/$', views.post_list , name="list"),
    url(r'^detail/(?P<post_id>\d+)/$', views.post_detail , name="detail"),

    url(r'^create/$', views.post_create , name="create"),
    url(r'^update/(?P<post_id>\d+)/$', views.post_update , name="update"),
    url(r'^delete/(?P<post_id>\d+)/$', views.post_delete , name="delete"),
]