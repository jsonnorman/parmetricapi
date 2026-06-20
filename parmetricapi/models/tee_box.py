from django.db import models
from .course import Course


class TeeBox(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    color = models.CharField(max_length=20)
    total_yardage = models.IntegerField()
