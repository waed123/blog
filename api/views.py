from posts.models import Post 
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsAuthor
from rest_framework.generics import ListAPIView,RetrieveAPIView, DestroyAPIView, CreateAPIView, RetrieveUpdateAPIView
from .serializers import UserLoginSerializer, PostListSerializer, PostDetailSearializer, PostCreateUpdateSearializer, CommentListSerializer, CommentCreateSerializer, UserCreateSerializer
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from django_comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response


class UserLoginAPIView(APIView):
	permission_classes = [AllowAny]
	serializer_class = UserLoginSerializer

	def post(self, request, format=None):
		data = request.data
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data=serializer.data
			return Response(new_data, status=HTTP_200_OK) #successful response
		return Response(serializer.errors, Http_400_BAD_REQUEST)


class UserCreateAPIView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserCreateSerializer



class CommentListView(ListAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentListSerializer
	permission_classes = [AllowAny]

	def get_queryset(self, *args, **kwargs):
		queryset = Comment.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset = queryset.filter(
				Q(object_pk=query)|
				Q(user=query)
				).distinct()
		return queryset



class CommentCreateAPIView(CreateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentCreateSerializer
	permission_classes = [IsAuthenticated]


	def perform_create(self, searializer):
		searializer.save(
			content_type=ContentType.objects.get_for_model(Post),
			sites=Site.objects.get(id=1),
			user=self.request.user,
			user_name=self.request.user.username,
			submit_date=timezone.now()
			)

	

class PostListAPIView(ListAPIView):
	# we should give value to queryset and serializer_class variable that exist in ListAPIView
	queryset = Post.objects.all() 
	serializer_class = PostListSerializer
	#fixed because it is inherited 
	#http://127.0.0.1:8000/api/?search=post 
	#http://127.0.0.1:8000/api/?ordering=title or -title
	filter_backends = [SearchFilter, OrderingFilter] 
	search_fields = ['title', 'content', 'author__first_name']
	permission_classes = [AllowAny]

	# override get_queryset fun to search in the list of objects using url
	#http://127.0.0.1:8000/api/?q=img
	#http://127.0.0.1:8000/api/?q=img&search=post
	def get_queryset(self, *args, **kwargs):
		queryset = Post.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset = queryset.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)
				).distinct()
		return queryset

class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSearializer
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'

	permission_classes = [AllowAny]




class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSearializer
	lookup_field = 'slug'    
	lookup_url_kwarg = 'post_slug'

	permission_classes = [IsAuthenticated, IsAdminUser]

class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSearializer
	lookup_field = 'slug'    
	lookup_url_kwarg = 'post_slug'

	permission_classes = [IsAuthenticated, IsAuthor]

class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSearializer

	#override to change the value of author before save the object
	def perform_create(self, searializer):
		searializer.save(author=self.request.user)

	permission_classes = [IsAuthenticated]
	
