from django.shortcuts import render, redirect

from .models import Post
from .forms import PostForm
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote

from django.http import Http404





def post_list(request):
	objects = Post.objects.all()
	#objects = Post.objects.all().oredr_by('title', 'id')

	#paginations
	paginator = Paginator(objects, 4) # Show 25 contacts per page

	number = request.GET.get('page')

	try:
		objects = paginator.page(number)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		objects = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		objects = paginator.page(paginator.num_pages)

	context = {
		"post_items": objects,
	}
	return render (request, "list.html", context)




def post_detail(request, post_slug):
	item = Post.objects.get(slug=post_slug)
	# item = Post.objects.get_object_or_404(Post, id=1000)
	context = {
		"item": item,
		"share_string": quote(item.content),
	}
	return render (request, "detail.html", context)







def post_create(request):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None )
	if form.is_valid():
		form.save()
		messages.success(request, "Added Successfully :)")
		return redirect("more:list")
	context = {
		'form': form
	}
	return render (request, "post_create.html", context)






def post_update(request, post_slug):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	item = Post.objects.get(slug=post_slug)
	form = PostForm(request.POST or None,request.FILES or None ,instance = item)

	if form.is_valid():
		form.save()
		messages.info(request, "Updated Successfully :)")
		return redirect("more:list")
	context = {
		'form': form,
		"item": item,
	}
	return render (request, "post_update.html", context)






def post_delete(request, post_slug):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	item = Post.objects.get(slug=post_slug).delete()
	messages.warning(request, "Noooooooo :(")
	return redirect("more:list")





