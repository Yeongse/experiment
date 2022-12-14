from django.db import models

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=8)

    def __str__(self):
        return self.name

class Choice(models.Model):
    attribute_num = models.IntegerField()
    choice = models.CharField(max_length=8)
    score = models.IntegerField()
    ignore = models.CharField(max_length=255)
    comment = models.TextField(null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="choices")

    def __str__(self):
        return f"{self.attribute_num}属性,  {self.score}点, {self.ignore}"

class Weight(models.Model):
    avg = models.FloatField()
    hr = models.FloatField()
    sb = models.FloatField()
    defense = models.FloatField()
    rbi = models.FloatField()
    bb = models.FloatField()
    risp = models.FloatField()
    dp = models.FloatField()
    disabled = models.FloatField()
    age = models.FloatField()
    CI = models.FloatField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="weight")

    def __str__(self):
        return f"CI: {self.CI}"

class Preference(models.Model):
    four = models.FloatField()
    six = models.FloatField()
    eight = models.FloatField()
    ten = models.FloatField()
    CI = models.FloatField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="preference")
    
    def __str__(self):
        return f"CI: {self.CI}"

class Player(models.Model):
    avg = models.FloatField()
    hr = models.FloatField()
    sb = models.FloatField()
    defense = models.FloatField()
    rbi = models.FloatField()
    bb = models.FloatField()
    risp = models.FloatField()
    dp = models.FloatField()
    disabled = models.FloatField()
    age = models.FloatField()

    def __str__(self):
        return f"打率: {self.avg}, ホームラン: {self.hr}本"