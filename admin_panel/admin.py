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
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px;" '
                'class="image-preview" id="image-preview-{}"/>',
                obj.image.url,
                obj.id or '__prefix__'
            )
        return format_html(
            '<img class="image-preview" id="image-preview-{}" '
            'style="max-width: 150px; max-height: 150px;" />',
            obj.id or '__prefix__'
        )
    image_preview.short_description = 'Image Preview'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'latitude', 'longitude',
                    'create_date', 'update_date')
    list_display_links = ('name',)
    readonly_fields = ('create_date', 'update_date')
    list_filter = ('type',)
    search_fields = ('name',)
    fieldsets = (
        ('Location Details', {
            'fields': ('name', 'type', 'latitude', 'longitude',)
        }),
        ('Timestamps', {
            'fields': ('create_date', 'update_date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'update_date')
    readonly_fields = ('create_date', 'update_date')
    search_fields = ('name',)

    fieldsets = (
        ('Amenity name', {
            'fields': ('name',)
        }),
        ('Timestamps', {
            'fields': ('create_date', 'update_date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('display_featured_image', 'property_id', 'title',
                    'display_locations', 'display_amenities',
                    'create_date', 'update_date')
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

    def display_amenities(self, obj):
        # Display first 3 amenities
        return ", ".join([amenity.name for amenity in obj.amenities.all()[:3]])
    display_amenities.short_description = 'Amenities'  # Sets column header

    def display_locations(self, obj):
        return ", ".join([location.name for location in obj.locations.all()])
    display_locations.short_description = 'Locations'

    def display_featured_image(self, obj):
        featured_image = obj.images.filter(is_featured=True).first()
        if featured_image:
            return format_html(
                '<img src="{}" width="80" height="60" '
                'style="object-fit: cover;" />',
                featured_image.image.url
            )
        return "No featured image"

    display_featured_image.short_description = 'Featured Image'


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'property', 'caption',
                    'is_featured', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    list_filter = ('property__title', 'is_featured')
    # ordering = ('property',)  orders the images as the properties are
    search_fields = ('property__title', 'property__property_id')
    list_display_links = ('property',)
    fieldsets = (
        (None, {
            'fields': ('property', 'image', 'image_preview',
                       'caption', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" width="180" height="180" '
                'style="object-fit: cover;" id="preview-{}" />'
                '</a>',
                obj.image.url, obj.image.url, obj.id or '__new__'
            )

        return format_html(
            '<img src="" width="200" height="200" '
            'style="display:none;" id="preview-{}" />',
            obj.id or '__new__'
        )

    image_preview.short_description = 'Image Preview'

    class Media:
        js = ('js/admin/property_image_preview.js',)
