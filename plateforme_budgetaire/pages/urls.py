from django.conf.urls import patterns, url
from pages import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
)
