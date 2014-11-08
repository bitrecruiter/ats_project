from django.conf.urls import patterns, include, url
from ats.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bcauth_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^job/(?P<job_id>\d+)/', JobView.as_view(), name='ats_job'),
    url(r'^jobs/', JobListView.as_view(), name='ats_jobs'),
    url(r'^applicants/', ApplicantListView.as_view(), name='ats_applicants'),
    url(r'^create/', JobCreateView.as_view(), name='ats_create'),
    url(r'^users/', UserListView.as_view(), name='ats_users'),
    url(r'^osrc/', GitHubListView.as_view(), name='ats_osrc'),
    url(r'^apply/(?P<job_id>\d+)/', ApplyView.as_view(), name='ats_apply'),
)
