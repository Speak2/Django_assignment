from django.contrib import admin
from .models import Location, Amenity, Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'title', 'create_date', 'update_date')
    list_filter = ('locations', 'amenities')
    search_fields = ('property_id', 'title', 'description')
    filter_horizontal = ('locations', 'amenities')
    readonly_fields = ('create_date', 'update_date')
    inlines = [PropertyImageInline]

    fieldsets = (
        ('Property Details', {
            'fields': ('property_id', 'title', 'description')
        }),
        ('Relationships', {
            'fields': ('locations', 'amenities')
        }),
        ('Timestamps', {
            'fields': ('create_date', 'update_date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'latitude', 'longitude')
    list_filter = ('type',)
    search_fields = ('name',)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image')
    list_filter = ('property',)
    search_fields = ('property__title', 'property__property_id')
