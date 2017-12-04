from rest_framework import serializers
from posts.models import Post
from django_comments.models import Comment
from django.contrib.auth.models import User

class UserLoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	def validate(self, data):
		username = data.get('username')
		password = data.get('password')

		if username == '':
			raise serializers.ValidationError("A username is required to login.")

		user = User.objects.filter(username=username)
		if user.exists():
			user_obj=user.first() #since User.objects.filter(username=username) return a list so I need to choose 1 obj from the list to assign it
		else:
			raise serializers.ValidationError("This username does not exist.")

		if user_obj:
			# check_password is a method from user model allows me to check if it is the correct password or not
			if not user_obj.check_password(password):
				raise serializers.ValidationError("This credentials, please try again.")
		return data




#to display extra author data
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['email', 'username', 'first_name', 'last_name']

#to make users to register for our site through our API
class UserCreateSerializer(serializers.ModelSerializer):
	#when overriding the field I should do that before meta
	#hide password on typing & not see the password in response on API 
	password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = User
		fields = ['username', 'email', 'password']

	#& in admin page password not saved since its not hashed/encroybted
	def create(self, validate_data):
		#validated_data is a dictionary that holds the data that was submitted to the serializer and validated
		username = validate_data['username']
		email = validate_data['email']
		password = validate_data['password']
		#I can use user.objects.create to create and save user at the same time but when using User(username=username) I need to save it after that 
		new_user = User(username=username, email=email) 
		new_user.set_password(password)
		new_user.save()
		return validate_data




class CommentListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ["object_pk", "user", "comment", "submit_date"]

# object_pk is the id of post object that I commented on it 
class CommentCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ["object_pk", "comment",]




class PostListSerializer(serializers.ModelSerializer):
	#to display name of author not id or to display another column with specific data I need to use SerializerMethodField
	#author = serializers.SerializerMethodField()

	#to display extra author data
	author = UserSerializer()

	#link to detail page
	detail_page = serializers.HyperlinkedIdentityField(
		view_name = "api:detail",
		lookup_field = "slug",
		lookup_url_kwarg = "post_slug",
		)
	delete_page = serializers.HyperlinkedIdentityField(
		view_name = "api:delete",
		lookup_field = "slug",
		lookup_url_kwarg = "post_slug",
		)
	update_page = serializers.HyperlinkedIdentityField(
		view_name = "api:update",
		lookup_field = "slug",
		lookup_url_kwarg = "post_slug",
		)
	class Meta:
		model = Post
		fields = ['title', 'author','publish', 'slug', 'detail_page', 'delete_page', 'update_page']

	# def get_author(self, obj):
	# 	return str(obj.author.username)



class PostDetailSearializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()
	comments = serializers.SerializerMethodField()
	
	class Meta:
		model = Post
		fields = ['id','author', 'user','title', 'slug', 'content','publish','draft', 'image', 'comments']

	def get_user(self, obj):
		return str(obj.author.username)

	def get_comments(self, obj):
		comment_list = Comment.objects.filter(object_pk=obj.id)
		comments = CommentListSerializer(comment_list, many=True).data
		return comments



class PostCreateUpdateSearializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['title', 'content', 'publish', 'draft', 'img']