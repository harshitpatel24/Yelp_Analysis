from django.shortcuts import render

# Create your views here.
from login_register.models import users


def homepage(request):
    if 'userid' in request.session:
        user_object = users.objects.get(pk=request.session['userid'])
        args = {'user_object': user_object, 'logged_in': 1}
    else:
        args = {'logged_in': 0}
    return render(request, 'home/homepage.html', args)