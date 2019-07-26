from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^leave_org/(?P<org_id>\d+)$', views.leave_org),
    url(r'^join_org/(?P<org_id>\d+)$', views.join_org),
    url(r'^org_info/(?P<org_id>\d+)$', views.org_info),
    url(r'^create_org$', views.create_org),
    url(r'^remove_org/(?P<org_id>\d+)$', views.remove_org),
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^login_user$', views.login_user),
    
]