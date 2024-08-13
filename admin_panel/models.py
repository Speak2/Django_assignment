from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=[
        ('country', 'Country'),
        ('state', 'State'),
        ('city', 'City'),
    ])
    latitude = models.FloatField()
    longitude = models.FloatField()

    def clean(self):
        if not (-90 <= self.latitude <= 90):
            raise ValidationError('Latitude must be between -90 and 90.')
        if not (-180 <= self.longitude <= 180):
            raise ValidationError('Longitude must be between -180 and 180.')

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    class Meta:
        verbose_name_plural = "Locations"


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def clean(self):
        # Ensure the name field doesn't contain any numbers
        if re.search(r'\d', self.name):
            raise ValidationError(_('Amenity name cannot contain numbers'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"


class Property(models.Model):
    property_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    locations = models.ManyToManyField(Location)
    amenities = models.ManyToManyField(Amenity)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.id:  # If the object already exists
            self.update_date = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Properties"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images',
                                 on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property.title}"
