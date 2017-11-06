from django.contrib import admin

# Register your models here.
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
	list_display = ['title', 'updated' , 'content']
	search_fields = ['title', 'content']
	list_filter = ['title']
	list_display_links = ['updated']
	list_editable = ['content']

	class Meta:
		model = Post

admin.site.register(Post, PostModelAdmin)