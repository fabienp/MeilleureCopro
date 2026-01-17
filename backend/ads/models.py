from django.db import models

class RealEstateAd(models.Model):
    bienici_id = models.CharField(max_length=100, unique=True)
    condo_fees = models.FloatField()
    department = models.CharField(max_length=3)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
