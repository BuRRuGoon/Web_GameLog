from django.db import models

class Steam(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    nowCurrent = models.IntegerField()
    fullCurrent = models.IntegerField()
    steamGameKey = models.IntegerField()
    iconUrl = models.CharField(max_length=300)

    class Meta:
        db_table = 'steam'

class Online(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    iconUrl = models.CharField(max_length=300)

    class Meta:
        db_table = 'online'

class Mobile(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    google = models.IntegerField()
    apple = models.IntegerField()
    one = models.IntegerField()
    iconUrl = models.CharField(max_length=300)

    class Meta:
        db_table = 'mobile'