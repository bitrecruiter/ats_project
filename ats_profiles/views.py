from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import View
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from ats_profiles.models import UserProfile, UserProfileAttachedFile
from ats_profiles.forms import UserProfileForm, UserNoteForm, UserProfileAttachedFileForm
from ats.models import UserNote


class UserProfileUpdateView(UpdateView):
    template_name = 'ats_profiles/edit_profile.html'
    success_url = '/profile/create'
    form_class = UserProfileForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfileUpdateView, self).dispatch(
            request,
            *args,
            **kwargs
        )

    def get_object(self, queryset=None):
        obj = UserProfile.objects.get_or_create(
            user=self.request.user
        )[0]
        return obj


class UserProfileAttachedFileDelete(DeleteView):
    model = UserProfileAttachedFile
    success_url = reverse_lazy('ats_profiles_edit')


class UserProfileAttachedFileCreate(CreateView):
    form_class = UserProfileAttachedFileForm
    template_name = 'ats_profiles/userprofileattachedfile_form.html'
    fields = ['file']

    def form_valid(self, *args, **kwargs):
        result = super(UserProfileAttachedFileCreate, self).form_valid(*args, **kwargs)
        userprofile = UserProfile.objects.get(user=self.request.user)
        userprofile.attached_files.add(self.object)
        userprofile.save()
        return result

    def get_success_url(self):
        return reverse('ats_profiles_edit')


class UserProfileEditView(View):
    template_name = 'ats_profiles/edit_profile.html'

    def get(self, request, *args, **kwargs):
        profile = UserProfile.objects.get_or_create(
            user=self.request.user
        )[0]
        return render_to_response(
            self.template_name,
            {
                'user': self.request.user,
                'form': UserProfileForm(instance=profile),
                'fileform': UserProfileAttachedFileForm()
            },
            context_instance=RequestContext(request)
        )

class UserProfileView(View):
    template_name = 'ats_profiles/view_profile.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        note = UserNote.objects.get_or_create(
            user_noter=self.request.user,
            user_noted=user,
        )[0]
        return render_to_response(
            self.template_name,
            {
                'profile_user': user,
                'note': note.note,
                'form': UserNoteForm(initial={'note': note.note}),
            },
            context_instance=RequestContext(request)
        )


class UserNoteUpdateView(UpdateView):
    model = UserProfile
    template_name = 'ats_profiles/edit_profile.html'
    success_url = '/profile/create'
    form_class = UserNoteForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserNoteUpdateView, self).dispatch(
            request,
            *args,
            **kwargs
        )

    def get_object(self, queryset=None):
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        obj = UserNote.objects.get_or_create(
            user_noter=self.request.user,
            user_noted=user,
        )[0]
        return obj

    def get_success_url(self):
        return reverse(
            'ats_profiles_view',
            kwargs={'user_id': self.kwargs['user_id']}
        )
