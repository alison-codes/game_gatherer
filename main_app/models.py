from django.db import models
from django.urls import reverse

OPTIONS = (
    ('T', True),
    ('F', False),
)

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=350)
    year_created = models.IntegerField()
    
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

# class Feeding(models.Model):
#   date = models.DateField()
#   meal = models.CharField(
#     max_length=1,
# 	 choices=MEALS,
# 	 default=MEALS[0][0]
#   )
#   game = models.ForeignKey(Game, on_delete=models.CASCADE)

#   def __str__(self):
#     return f"{self.get_meal_display()} on {self.date}"