from django.db import models

class Recipe(models.Model):
    image = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=300)
    viewcount = models.CharField(max_length=50)

    def __str__(self):
        return self.title