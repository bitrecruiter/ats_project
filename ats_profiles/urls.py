from django.conf.urls import patterns, include, url
from ats_profiles.views import UserProfileEditView, UserProfileView, UserNoteUpdateView, UserProfileUpdateView, UserProfileAttachedFileCreate, UserProfileAttachedFileDelete

urlpatterns = patterns(
    '',
    url(
        r'^create/',
        UserProfileEditView.as_view(),
        name='ats_profiles_edit'
    ),
    url(
        r'^view/(?P<user_id>\d+)/',
        UserProfileView.as_view(),
        name='ats_profiles_view'
    ),
    url(
        r'^note/(?P<user_id>\d+)/',
        UserNoteUpdateView.as_view(),
        name='ats_profiles_note'
    ),
    url(
        r'^note/(?P<user_id>\d+)/',
        UserNoteUpdateView.as_view(),
        name='ats_profiles_note'
    ),
    url(
        r'^profileform/',
        UserProfileUpdateView.as_view(),
        name='ats_profiles_form'
    ),
    url(
        r'^fileform/',
        UserProfileAttachedFileCreate.as_view(),
        name='ats_profiles_fileform'
    ),
    url(
        r'^deletefile/(?P<pk>[\w]+)/$',
        UserProfileAttachedFileDelete.as_view(),
        name='ats_profiles_deletefile'
    ),
)
