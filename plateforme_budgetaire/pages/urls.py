from django.conf.urls import patterns, url
from pages import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^mission', views.mission, name='mission'),
    url(r'^register$', views.Register.as_view(), name='register'),
)
