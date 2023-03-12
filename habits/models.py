from django.db import models
from users.models import NULLABLE, User
from django.core.validators import MinValueValidator, MaxValueValidator


class Habits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_to_do = models.TimeField()
    action = models.CharField(max_length=254)
    place_to_do = models.CharField(max_length=254, **NULLABLE)
    reward = models.CharField(max_length=254, **NULLABLE)

    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE)

    is_related = models.BooleanField()
    is_private = models.BooleanField(default=True)

    periodicity = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(7), MinValueValidator(1)],
    )
    time_for_execute = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(120), MinValueValidator(1)],
    )

