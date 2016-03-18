from django.conf.urls import patterns, url
from project import views

urlpatterns = patterns(
    '',
    url(r'(?P<validated>0|1|2)/$', views.ProjectList.as_view(), name='project_list'),
    url(r'$', views.ProjectList.as_view(), {"validated": "all"}, name='project_list'),
)
