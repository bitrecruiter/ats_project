from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Job(models.Model):
    company = models.CharField(max_length=256)
    job_title = models.CharField(max_length=256)
    apply_identifier = models.CharField(max_length=256)
    job_description = models.TextField()
    location = models.CharField(max_length=256)
    reference_number = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s at %s' % (self.job_title, self.company)

    def get_absolute_url(self):
        return reverse('ats_job', kwargs={'job_id': self.id})


class Application(models.Model):
    user = models.ForeignKey(User)
    job = models.ForeignKey(Job)


class UserNote(models.Model):
    user_noted = models.ForeignKey(User, related_name='user_noted')
    user_noter = models.ForeignKey(User, related_name='user_noter')
    note = models.TextField()


class GitHubCache(models.Model):
    query = models.CharField(max_length=256)
    page = models.IntegerField()
    data = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
