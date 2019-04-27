from django.conf.urls import url

from analysis import views

urlpatterns = [
    url(r'^step-1$', views.step1, name='step_1'),
    url(r'^step-2$', views.step2, name='step_2'),
    url(r'^visualization$', views.visualization, name='visulaization'),
    url(r'^filter_data$', views.filter_data, name='filter data'),
    url(r'^rating_dist$', views.rating_dist, name ='rating_dist'),
    url(r'^top_businesses/+(?P<category>\d+)+$', views.top_businesses, name ='top_businesses'),
    url(r'^top_business_categories/+(?P<category>\d+)+$', views.top_business_categories, name ='business_categories'),
    url(r'^five_star_businesses/+(?P<category>\d+)+$', views.five_star_businesses, name ='five_star_businesses')

]