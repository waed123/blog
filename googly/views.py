
from django.http import JsonResponse
from django.shortcuts import render
import requests

def place_text_search(request):
	key = "AIzaSyDdxE9l_bwR6oE16yGPLPZWnrHaUh4lXjc" #authenticate to access google api
	#query = "bank"
	query=request.GET.get('query', 'bank') #query is the thing that what you want to search about  # first arg is the html input element name , second is the default value if there is no data in query 
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&region=kw&key=%s"%(query, key)

	next_page = request.GET.get('nextpage')
	if next_page is not None:
		url += "&pagetoken=" + next_page # add the string to the end of url

	response = requests.get(url)

	context = {
		"response" : response.json(),
	}
	#return JsonResponse(response.json(), safe=False)
	return render(request, "place_search.html", context)


def place_detail(request):
	key = "AIzaSyDdxE9l_bwR6oE16yGPLPZWnrHaUh4lXjc"
	place_id = request.GET.get('place_id', '')
	url = "https://maps.googleapis.com/maps/api/place/details/json?key=%s&placeid=%s"%(key,place_id)

	response = requests.get(url)
	map_key = "AIzaSyD9pGoidGfHSyxhN_CcyRyHVWqVBoTbY14"

	context = {
		"response" : response.json(),
		"map_key": map_key,
	}

	#return JsonResponse(response.json(), safe=False)
	return render(request, "place_detail.html", context)