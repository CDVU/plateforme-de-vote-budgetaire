from django.conf.urls import patterns, url
from vote.views import *

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^form/$', Form.as_view(), name='form'),
)
