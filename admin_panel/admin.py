from django.contrib import admin
from .models import Location, Amenity, Property, PropertyImage
from django.utils.html import format_html


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ('image', 'image_preview', 'caption', 'is_featured')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 150px; max-height: 150px;" id="image-preview-{}"/>', obj.image.url, obj.id)
        return format_html('<img id="image-preview-{}" style="max-width: 150px; max-height: 150px;" />', obj.id)
    image_preview.short_description = 'Image Preview'

    class Media:
        js = ('js/admin/image_preview.js',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'latitude', 'longitude')
    list_display_links = ('name',)
    list_filter = ('type',)
    search_fields = ('name',)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'title', 'create_date', 'update_date')
    list_display_links = ('title',)
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


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image_preview', 'caption', 'is_featured', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('property__title', 'is_featured')
    # ordering = ('property',)  orders the images as the properties are ordered in the properties table
    search_fields = ('property__title', 'property__property_id')
    list_display_links = ('property',)
    fieldsets = (
        (None, {
            'fields': ('property', 'image', 'caption', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            # The URL should be relative to MEDIA_URL
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" width="200" height="200" /></a>',
                obj.image.url,  obj.image.url
            )
        return "No Image"
    image_preview.short_description = 'Image Preview'
