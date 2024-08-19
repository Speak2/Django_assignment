from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


class Location(models.Model):
    name = models.CharField(max_length=100, blank=False)
    type = models.CharField(max_length=20, choices=[
        ('country', 'Country'),
        ('state', 'State'),
        ('city', 'City'),
    ])
    latitude = models.FloatField(blank=False, null=False)
    longitude = models.FloatField(blank=False, null=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True, blank=True)

    def clean(self):
        # Validate latitude and longitude ranges
        if self.latitude is not None and not (-90 <= self.latitude <= 90):
            raise ValidationError(
                {'latitude': _('Latitude must be between -90 and 90.')})
        if self.longitude is not None and not (-180 <= self.longitude <= 180):
            raise ValidationError(
                {'longitude': _('Longitude must be between -180 and 180.')})

        # Validate that the name only contains letters
        if not re.match(r'^[A-Za-z]+$', self.name):
            raise ValidationError(_('Amenity name must contain only letters'))

        # Check for duplicate rows
        if Location.objects.filter(
            name=self.name,
            type=self.type,
            latitude=self.latitude,
            longitude=self.longitude
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                'A same location already exists'
            )

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    def save(self, *args, **kwargs):
        if self.id:  # If the object already exists
            self.update_date = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Locations"


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True, blank=True)

    def clean(self):
        # Ensure the name field only contains letters
        if not re.match(r'^[A-Za-z]+$', self.name):
            raise ValidationError(_('Amenity name must contain only letters'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id:  # If the object already exists
            self.update_date = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Amenities"


class Property(models.Model):
    property_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    locations = models.ManyToManyField(Location)
    amenities = models.ManyToManyField(Amenity, blank=True)
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
    property = models.ForeignKey(
        Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    caption = models.CharField(
        max_length=255, null=True, blank=True, default=None)  # Default to null
    is_featured = models.BooleanField(default=False)  # Default to False

    def save(self, *args, **kwargs):
        if self.id:  # If the object already exists
            self.updated_at = timezone.now()

        super().save(*args, **kwargs)
