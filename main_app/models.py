from django.db import models
from django.urls import reverse

OPTIONS = (
    ('T', True),
    ('F', False),
)

# Create your models here.

class Adj(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse('adjs_detail', kwargs={'pk': self.id})

class Game(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=350)
    year_created = models.IntegerField()
    adjs = models.ManyToManyField(Adj)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'game_id': self.id})


class Played(models.Model):
    date = models.DateField('played date')
    won = models.CharField(
        max_length=5,
        choices=OPTIONS,
	    default=OPTIONS[0][0]
  )
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}"

    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for game_id: {self.game_id} @{self.url}"
