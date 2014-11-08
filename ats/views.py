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
from ats.models import Job, Application, GitHubCache
from ats.forms import SearchForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.timezone import utc
from math import ceil
import requests
import datetime
import json

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
                job__job_title__contains=form.cleaned_data['query']
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


class GitHubListView(FormMixin, View):
    template_name = 'ats/users.html'
    paginate_by = 10
    context_object_name = 'users_list'
    form_class = SearchForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GitHubListView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        return {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
            'data': self.request.GET or None
        }

    def github_search(self, query, page):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        try:
            g = GitHubCache.objects.get(query=query, page=page)
        except GitHubCache.DoesNotExist:
            g = GitHubCache()
            g.query = query
            g.page = page
        if not g.created_at or (now - g.created_at).total_seconds() > 3600:
            # Check to make sure we aren't exceeding githubs rate limiting
            c = GitHubCache.objects.filter(
                created_at__gt=now-datetime.timedelta(minutes=1)
            ).count()
            if c >= 5:
                if g.data:  # Past rate limit and have an old cache? serve it.
                    return json.loads(g.data)
                else:
                    return False
            payload = {
                'q': query,
                'sort': 'stars',
                'per_page': self.paginate_by,
                'page': page
            }
            r = requests.get(
                'https://api.github.com/search/repositories',
                params=payload
            )
            g.data = r.text
            g.save()
        return json.loads(g.data)

    def get(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        if form.is_valid() and form.cleaned_data['query'] != '':
            query = form.cleaned_data['query']
            page = int(form.data['page'])
            if page * self.paginate_by > 1000:
                page = 1000 / self.paginate_by

            j=self.github_search(query, page)
            if not j:
                context = {'error': 'Failed to query github, try again.', 'query': query}
                return render_to_response(self.template_name, context, context_instance=RequestContext(request))

            object_list = []
            for item in j['items']:
                object_list.append({
                    'user': item['owner']['login'],
                    'tag': item['language'],
                    'github': True
                })

            page_obj = {}
            page_obj['num_pages'] = int(ceil(j['total_count'] / float(self.paginate_by)))
            if page_obj['num_pages'] * self.paginate_by > 1000:
                page_obj['num_pages'] = 1000 / self.paginate_by
            page_obj['number'] = page
            if page >= page_obj['num_pages']:
                page_obj['number'] = page_obj['num_pages']
                page_obj['has_next'] = False
                page_obj['next_page_number'] = page_obj['num_pages']
            else:
                page_obj['next_page_number'] = page+1
                page_obj['has_next'] = True

            if page <= 1:
                page_obj['number'] = 1
                page_obj['has_previous'] = False
                page_obj['previous_page_number'] = 1
            else:
                page_obj['has_previous'] = True
                page_obj['previous_page_number'] = page-1

            context = self.get_context_data(form=form, query=query, users_list=object_list, is_paginated=True, page_obj=page_obj)
            return render_to_response(self.template_name, context, context_instance=RequestContext(request))
        return render_to_response(self.template_name, {}, context_instance=RequestContext(request))


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
