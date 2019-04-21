from django.conf.urls import url

from login_register import views

urlpatterns = [
    url(r'^register_page$', views.show_register_page, name='register_page'),
    url(r'^save_info$', views.save_info, name='save_info'),
    url(r'^login_page$', views.show_login_page, name='login_page'),
    url(r'^check_info$', views.check_info, name='check_info'),
    url(r'^sign_out$', views.sign_out, name='sing_out')
]