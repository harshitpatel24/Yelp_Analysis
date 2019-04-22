from django.conf.urls import url

from analysis import views

urlpatterns = [
    url(r'^step-1$', views.step1, name='step_1'),

]