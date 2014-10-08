from django.shortcuts import render_to_response
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.template import RequestContext
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin
from django.db.models import Q
from ats.models import Job, Application
from ats.forms import SearchForm
from django.contrib.sites.shortcuts import get_current_site

"""class JobListView(ListView):
    model = Job
    template_name = 'ats/jobs.html'
    paginate_by = 10
    context_object_name = 'job_list'"""


class JobListView(FormMixin, ListView):
    model = Job
    template_name = 'ats/jobs.html'
    paginate_by = 10
    context_object_name = 'job_list'
    form_class = SearchForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(JobListView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        return {
          'initial': self.get_initial(),
          'prefix': self.get_prefix(),
          'data': self.request.GET or None
        }

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        form = self.get_form(self.get_form_class())
        query = ''

        if form.is_valid() and form.cleaned_data['query'] != '':
            self.object_list = self.object_list.filter(
                job_title__contains=form.cleaned_data['query']
            )
            query = form.cleaned_data['query']
        context = self.get_context_data(form=form, query=query)
        return self.render_to_response(context)


class JobView(View):
    template_name = 'ats/job.html'

    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, pk=kwargs['job_id'])
        return render_to_response(
            self.template_name,
            {'job': job},
            context_instance=RequestContext(request)
        )


class ApplicantListView(FormMixin, ListView):
    model = Application
    template_name = 'ats/applicants.html'
    paginate_by = 10
    context_object_name = 'applicant_list'
    form_class = SearchForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ApplicantListView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        return {
          'initial': self.get_initial(),
          'prefix': self.get_prefix(),
          'data': self.request.GET or None
        }

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        form = self.get_form(self.get_form_class())
        query = ''

        if form.is_valid() and form.cleaned_data['query'] != '':
            self.object_list = self.object_list.filter(
                user__username__contains=form.cleaned_data['query']
            )
            query = form.cleaned_data['query']
        context = self.get_context_data(form=form, query=query)
        return self.render_to_response(context)

class JobCreateView(CreateView):
    model = Job
    template_name = 'ats/create_job.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(JobCreateView, self).dispatch(*args, **kwargs)


class UserListView(FormMixin, ListView):
    model = User
    template_name = 'ats/users.html'
    paginate_by = 10
    context_object_name = 'users_list'
    form_class = SearchForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserListView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        return {
          'initial': self.get_initial(),
          'prefix': self.get_prefix(),
          'data': self.request.GET or None
        }

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        form = self.get_form(self.get_form_class())
        query = ''
        if form.is_valid() and form.cleaned_data['query'] != '':
            self.object_list = self.object_list.filter(
                reduce(
                    lambda x, y: x | y, [Q(userprofile__cvtext__contains=word) for word in form.cleaned_data['query'].split()]
                )
            )
            query = form.cleaned_data['query']
        context = self.get_context_data(form=form, query=query)
        return self.render_to_response(context)


class ApplyView(View):
    template_name = 'ats/apply.html'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        job = get_object_or_404(Job, pk=kwargs['job_id'])
        Application.objects.create(user=request.user, job=job)
        return render_to_response(
            self.template_name,
            {
                'job': job,
                'applied': True
            },
            context_instance=RequestContext(request)
        )

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        job = get_object_or_404(Job, pk=kwargs['job_id'])
        try:
            Application.objects.get(user=request.user, job=job)
            applied = True
        except Application.DoesNotExist:
            applied = False
        return render_to_response(
            self.template_name,
            {
                'job': job,
                'applied': applied
            },
            context_instance=RequestContext(request)
        )
