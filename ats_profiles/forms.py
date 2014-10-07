from django import forms
from ats_profiles.models import UserProfile, UserProfileAttachedFile
from ats.models import UserNote


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
