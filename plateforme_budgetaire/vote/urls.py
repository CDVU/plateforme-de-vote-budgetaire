from django.conf.urls import patterns, url
from vote.views import *

urlpatterns = patterns(
    '',
    url(r'^$', Form.as_view(), name='form'),
)
