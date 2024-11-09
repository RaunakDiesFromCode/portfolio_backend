from django.db import models


class reviewForm(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    # Add other fields as necessary

    def __str__(self):
        return self.name
