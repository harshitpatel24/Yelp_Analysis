from django.conf.urls import url

from home import views

urlpatterns = [
    url(r'^homepage$', views.homepage, name='home_page'),
]