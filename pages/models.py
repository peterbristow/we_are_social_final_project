from __future__ import unicode_literals

from django.db import models


class ContactRequest(models.Model):
    """
    Define Email model
    """
    contact_name = models.CharField(max_length=255)
    contact_email = models.CharField(max_length=255)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.contact_name
