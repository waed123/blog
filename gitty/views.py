from django.shortcuts import render
from django.http import JsonResponse
import requests

def member_list(request):
	waed = request.user

	
	# to know which socail account that the user logged in by
	#to retrieve specific social account that user currently using to logged in fron a list of social accounts for that user 
	social_account = waed.socialaccount_set.get(user=waed.id) #relationship betwwen user and socialaccount foriegnkey - many socailaccounts to the user 
	
	#get specific social account token for the social account that I retrieved 
	social_token = social_account.socialtoken_set.get(account=social_account.id)
	token = social_token.token # to retrieve only the token field from social_token object

	#url = "https://api.github.com/orgs/joinCODED/members" #List all users who are members of an organization.
	url = "https://api.github.com/user/repos" # retrieve user/your repository
	response = requests.get(url, headers={"Authorization":"token " + token}) #headers is way to pass parameters to URL
	
	return JsonResponse(response.json(), safe=False)

