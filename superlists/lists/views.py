from django.shortcuts import render
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie


# Create your views here.

# @ensure_csrf_cookie
def home_page(request):
	if request.method == 'POST':
		# return HttpResponse(request.POST['item_text'])
		return render(
			request, 
			'home.html', 
			{
				'new_item_text': request.POST.get('item_text', ''),
			},
		)
	return render(request, 'home.html')