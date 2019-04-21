from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from login_register.models import users


def show_register_page(request):
    if 'userid' in request.session:
        return HttpResponseRedirect('/home/homepage')
    else:
        return render(request,'login_register/register_page.html')

def save_info(request):
    if 'userid' in request.session:
        return HttpResponseRedirect('/home/homepage')
    else:
        if request.method == 'POST':
            fname = request.POST.get('fname')
            lname=request.POST.get('lname')
            email=request.POST.get('email')
            password=request.POST.get('pass')

            user_object = users(fname=fname, lname=lname, email=email, password=password)
            user_object.save()
            request.session['userid'] = user_object.pk

        return HttpResponseRedirect('/home/homepage')

def show_login_page(request):
    if 'userid' in request.session:
        return HttpResponseRedirect('/home/homepage')
    else:
        return render(request,'login_register/login_page.html')


def check_info(request):
    if 'userid' in request.session:
        return HttpResponseRedirect('/home/homepage')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('pass')
            user_object = users.objects.get(email = email, password = password)
            if user_object is not None:
                request.session['userid'] = int(user_object.pk)
                return HttpResponseRedirect('/home/homepage')
            else:
                return HttpResponseRedirect('/login_register/login_page')


def sign_out(request):
    if 'userid' in request.session:
        del request.session['userid']
    return HttpResponseRedirect('/home/homepage')