from django.contrib import admin
from ats.models import Job


class JobAdmin(admin.ModelAdmin):
    # ...
    list_display = ('company', 'job_title', 'location', 'created_at')
admin.site.register(Job, JobAdmin)
