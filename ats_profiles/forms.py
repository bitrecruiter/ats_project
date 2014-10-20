from django import forms
from django.contrib.auth.models import User
from ats_profiles.models import UserProfile, UserProfileAttachedFile
from ats.models import UserNote


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude=('password', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'username', 'is_staff', 'is_active', 'date_joined')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'cvtext', 'attached_files', 'tags')


class UserNoteForm(forms.ModelForm):
    class Meta:
        model = UserNote
        exclude = ('user_noted', 'user_noter')


class UserProfileAttachedFileForm(forms.ModelForm):
    class Meta:
        model = UserProfileAttachedFile
