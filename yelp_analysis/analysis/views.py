from django.shortcuts import render

# Create your views here.
def step1(request):
    return render(request,'analysis/step-1.html')