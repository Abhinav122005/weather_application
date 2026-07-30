from django.db import models
from accounts.models import User

# Create your models here.
class FavoriteCity(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    city = models.CharField(max_length=100)

    class Meta:
        unique_together = ("user", "city")

    def __str__(self):
        return f"{self.user.username} - {self.city}"



class SearchHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    city = models.CharField(max_length=100)

    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.city}"