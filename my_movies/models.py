from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Movie(models.Model):
    """movie data"""
    title = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=1500)
    rating = models.FloatField(null=True, blank=True)
    review = models.CharField(null=True, blank=True, max_length=2000)
    img_url = models.URLField(null=True, blank=True, max_length=2000)
    homepage = models.URLField(null=True, blank=True, max_length=2000)

    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """return model as a string"""
        return self.title


class Comment(models.Model):
    """users' comments"""
    text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'comments'

    def __str__(self):
        """model as a string"""
        return f"{self.text[:50]}..."


