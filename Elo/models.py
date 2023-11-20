from django.db import models

# Create your models here.

class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    elo = models.DecimalField(default=500.0, decimal_places=1, max_digits=6)
    
    def __str__(self):
        return self.name
