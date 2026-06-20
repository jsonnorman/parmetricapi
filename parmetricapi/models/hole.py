from django.db import models
from .tee_box import TeeBox


class Hole(models.Model):
    tee_box = models.ForeignKey(TeeBox, on_delete=models.CASCADE)
    hole_number = models.IntegerField()
    yardage = models.IntegerField()
    par = models.IntegerField()
    handicap = models.IntegerField()
