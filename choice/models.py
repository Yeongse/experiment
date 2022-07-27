from django.db import models

# Create your models here.
class Subject(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name

class Choice(models.Model):
    attribute_num = models.IntegerField()
    choice = models.CharField()
    score = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="choices")

    def __str__(self):
        return f"{self.attribute_num}属性,  {self.choice}: {self.score}"

class Player(models.Model):
    avg = models.FloatField()
    hr = models.IntegerField()
    sb = models.IntegerField()
    defense = models.FloatField()
    rbi = models.IntegerField()
    bb = models.IntegerField()
    risp = models.FloatField()
    dp = models.IntegerField()
    disabled = models.FloatField()
    age = models.FloatField()

    def __str__(self):
        return f"打率: {self.avg}, ホームラン: {self.hr}本"