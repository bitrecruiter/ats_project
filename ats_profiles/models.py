from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from ats_profiles.get_docx_text import get_docx_text
from subprocess import Popen, PIPE
import os

def create_tags(sender, instance, **kwargs):
    tags = Tag.objects.all()
    for f in instance.attached_files.all():
        process = Popen(['unoconv', '--stdout', '--format=txt', f.file.path], stdout=PIPE)
        (data, err) = process.communicate()
        exit_code = process.wait()
        data = data.decode('utf-8').lower()
        for tag in tags:
            if tag.word.lower() in data:
                instance.tags.add(tag)
        instance.cvtext = data
    instance.save()


class Tag(models.Model):
    word = models.CharField(max_length=35)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.word


class UserProfileAttachedFile(models.Model):
    file = models.FileField()
    def filename(self):
        return os.path.basename(self.file.name)

    def __unicode__(self):
        return self.filename()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    SALUTATION_MR = 'Mr.'
    SALUTATION_MS = 'Ms.'
    SALUTATION_CHOICES = (
        (SALUTATION_MR, 'Mr.'),
        (SALUTATION_MS, 'Ms.'),
    )
    salutation = models.CharField(
        max_length=3,
        choices=SALUTATION_CHOICES,
        blank=True
    )
    address1 = models.CharField(max_length=256, blank=True)
    address2 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    postcode = models.CharField(max_length=32, blank=True)
    phone = models.CharField(max_length=256, blank=True)
    summary = models.CharField(max_length=256, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    cvtext = models.TextField(blank=True)
    wot_name = models.CharField(max_length=256, blank=True, default='')
    wot_rating = models.IntegerField(blank=True, default=0)
    attached_files = models.ManyToManyField(
        UserProfileAttachedFile,
        blank=True
    )

signals.m2m_changed.connect(
    create_tags,
    sender=UserProfile.attached_files.through
)
