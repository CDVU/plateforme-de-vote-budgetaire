from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'plateforme_budgetaire.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('pages.urls', namespace="pages")),
    url(r'^projects/', include('project.urls', namespace="projects")),
    url(r'^votes/', include('vote.urls', namespace="votes")),
]
