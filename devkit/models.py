from django.db import models

class PageViewCounter(models.Model):
    page_views = models.IntegerField(default=0)