from django.shortcuts import render

from .models import Post

def post_home(request):
	context = {
		"color" : ["Red", "White", "Blue"],
		"name" : "Toyota",
		"model" : "2017",
	}
	return render(request, 'post_create.html', context)

def post_list(request):
	objects = Post.objects.all()
	context = {
		"post_items": objects,
	}
	return render (request, "list.html", context)

def post_detail(request, post_id):
	item = Post.objects.get(id=post_id)
	# item = Post.objects.get_object_or_404(Post, id=1000)
	context = {
		"item": item,
	}
	return render (request, "detail.html", context)