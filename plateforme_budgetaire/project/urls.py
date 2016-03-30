from django.conf.urls import patterns, url
from project import views

urlpatterns = patterns(
    '',
    url(r'^view/(?P<pk>\d+)$', views.ProjectDetail.as_view(), name='project_detail'),
    url(r'^(?P<validated>0|1|2)$', views.ProjectList.as_view(), name='project_list'),
    url(r'^create/$', views.ProjectCreate.as_view(), name='project_create'),
    url(r'^list/$', views.ProjectList.as_view(), {"validated": "all"}, name='project_list'),
)
