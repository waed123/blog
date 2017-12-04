from django.conf.urls import url
from .views import UserLoginAPIView,PostListAPIView, PostDetailAPIView, PostDeleteAPIView, PostCreateAPIView, PostUpdateAPIView, CommentListView, CommentCreateAPIView, UserCreateAPIView


urlpatterns = [
	url(r'^$', PostListAPIView.as_view(), name="list"),
	url(r'^register/$', UserCreateAPIView.as_view(), name="register"),
	url(r'^login/$', UserLoginAPIView.as_view(), name="login"),
	url(r'^comments/$', CommentListView.as_view(), name="comment-list"),
	url(r'^comments/create/$', CommentCreateAPIView.as_view(), name="comment-create"),
	url(r'^create/$', PostCreateAPIView.as_view(), name="create"),
	url(r'^(?P<post_slug>[-\w]+)/detail/$', PostDetailAPIView.as_view(), name="detail"), 
	url(r'^(?P<post_slug>[-\w]+)/delete/$', PostDeleteAPIView.as_view(), name="delete"),
	url(r'^(?P<post_slug>[-\w]+)/update/$', PostUpdateAPIView.as_view(), name="update"),   
]