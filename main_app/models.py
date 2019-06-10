from django.db import models

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=350)
    year_created = models.IntegerField()
    
    def __str__(self):
        return self.name