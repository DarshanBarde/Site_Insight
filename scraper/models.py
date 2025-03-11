from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(unique=True)
    sitemap = models.TextField()  # Store URLs as JSON
    insights = models.TextField()  # AI-generated insights

    def __str__(self):
        return self.name
