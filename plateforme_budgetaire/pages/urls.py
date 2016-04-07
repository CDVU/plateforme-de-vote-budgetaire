from django.conf.urls import patterns, url
from pages import views

urlpatterns = patterns(
    '',
    url(r'^$', 'django.contrib.auth.views.login', name='home'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^mission', views.mission, name='mission'),
    url(r'^register/(.+)', views.RegisterValidation.as_view(), name='register_validation'),
    url(r'^register', views.Register.as_view(), name='register'),
    url(r'^logout$', views.logout_view, name='logout'),
)
