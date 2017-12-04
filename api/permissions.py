from rest_framework.permissions import BasePermission

class IsAuthor(BasePermission):
	message = "HaaaaaaHaaaa You dont have access" #override this the message that appear when if has_object_permission return False 

	def has_object_permission(self, request, view, obj):
		if (request.user == obj.author) or (request.user.is_staff):
			return True #give access to the user
		else:
			return False