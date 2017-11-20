from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import Like


def post_list(request):
	today = timezone.now().date()	
	objects = Post.objects.filter(draft=False, publish__lte=today)
	#objects = Post.objects.all().oredr_by('title', 'id')

	if request.user.is_staff:
		objects = Post.objects.all()

	query = request.GET.get('q')
	if query:
		objects = Post.objects.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(author__first_name__icontains=query)|
			Q(author__last_name__icontains=query)
			).distinct()

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
		"today": today,
	}
	return render (request, "list.html", context)






def post_detail(request, post_slug):
	item = Post.objects.get(slug=post_slug)
	# item = Post.objects.get_object_or_404(Post, id=1000)

	if not request.user.is_staff:
		if item.draft or item.publish > timezone.now().date():
			raise Http404

	if request.user.is_authenticated():
		if Like.objects.filter(post= item, user=request.user).exists():
			like = True
		else:
			like = False

	like_count = item.like_set.count()

	context = {
		"item": item,
		"liked": like,
		"like_count": like_count,
		"share_string": quote(item.content),
	}
	return render (request, "detail.html", context)




def post_create(request):
	if not (request.user.is_staff or request.user.is_superuser): # if not request.user.is_authenticated(): return 'login'
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None )
	if form.is_valid():
		item = form.save(commit=False)
		item.author = request.user
		item.save()
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



def like_button(request, post_id):
	post_object = Post.objects.get(id=post_id)
	like, created = Like.objects.get_or_create(user=request.user, post=post_object)

	if created:
		action="like"
	else:
		like.delete()
		action="unlike"

	like_count = post_object.like_set.count()
	response = {
		"action": action,
		"like_count": like_count,
	}
	return JsonResponse(response, safe=False)





