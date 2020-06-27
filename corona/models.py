from django.db import models


# Create your models here.
class Tickers(models.Model):
    class Meta:
        db_table = 'Tickers'
    symbol = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)


class ClosingPoints(models.Model):
    class Meta:
        db_table = 'ClosingPoints'
        unique_together = [['symbol', 'date']]
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=False)
    price = models.FloatField()


class VolumePoints(models.Model):
    class Meta:
        db_table = 'VolumePoints'
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=False)
    volume = models.FloatField()


class AvgVolume(models.Model):
    class Meta:
        db_table = 'AvgVolume'

    symbol = models.CharField(max_length=10, primary_key=True)
    day_avg_30 = models.FloatField(default=None, blank=True, null=True)
    day_avg_60 = models.FloatField(default=None, blank=True, null=True)
    day_avg_150 = models.FloatField(default=None, blank=True, null=True)
    total_avg = models.FloatField(default=None, blank=True, null=True)

class Earnings(models.Model):
    class Meta:
        db_table = 'Earnings'
    symbol = models.CharField(max_length=10, primary_key=True)
    zac_score = models.IntegerField(default=None, blank=True, null=True)
    zac_score_value = models.CharField(max_length=50,default=None, blank=True, null=True)
    upcoming_date = models.DateTimeField(auto_now_add=False,default=None, blank=True, null=True)
    upcoming_time = models.CharField(max_length=100,default=None, blank=True, null=True)

class Growth(models.Model):
    class Meta:
        db_table = 'Growth'
    symbol = models.CharField(max_length=10, primary_key=True)
    y_2015 = models.FloatField(default=None, blank=True, null=True)
    y_2016 = models.FloatField(default=None, blank=True, null=True)
    y_2017 = models.FloatField(default=None, blank=True, null=True)
    y_2018 = models.FloatField(default=None, blank=True, null=True)
    y_2019 = models.FloatField(default=None, blank=True, null=True)
    y_2020 = models.FloatField(default=None, blank=True, null=True)

class Statistics(models.Model):
    class Meta:
        db_table = 'Statistics'
    symbol = models.CharField(max_length=10, primary_key=True)
    mean_2015 = models.FloatField(default=None, blank=True, null=True)
    std_2015 = models.FloatField(default=None, blank=True, null=True)
    mean_2016 = models.FloatField(default=None, blank=True, null=True)
    std_2016 = models.FloatField(default=None, blank=True, null=True)
    mean_2017 = models.FloatField(default=None, blank=True, null=True)
    std_2017 = models.FloatField(default=None, blank=True, null=True)
    mean_2018 = models.FloatField(default=None, blank=True, null=True)
    std_2019 = models.FloatField(default=None, blank=True, null=True)
    mean_2019 = models.FloatField(default=None, blank=True, null=True)
    std_2019 = models.FloatField(default=None, blank=True, null=True)
    mean_2020 = models.FloatField(default=None, blank=True, null=True)
    std_2020 = models.FloatField(default=None, blank=True, null=True)

class DailyZScore(models.Model):
    class Meta:
        db_table = 'DailyZScore'
    symbol = models.CharField(max_length=10, primary_key=True)
    z_score = models.FloatField(default=None, blank=True, null=True)
