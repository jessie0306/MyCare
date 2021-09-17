from django.db import models

# Create your models here.
class Survey(models.Model):
    id = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    age = models.CharField(max_length=255, blank=True, null=True)
    shampoo = models.CharField(max_length=255, blank=True, null=True)
    perm = models.CharField(max_length=255, blank=True, null=True)
    dye = models.CharField(max_length=255, blank=True, null=True)
    current_hair = models.CharField(max_length=255, blank=True, null=True)
    product = models.CharField(max_length=255, blank=True, null=True)
    care_prefer = models.CharField(max_length=255, blank=True, null=True)
    buying_point = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'survey'