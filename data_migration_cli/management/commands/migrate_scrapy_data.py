from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
import psycopg2
from admin_panel.models import Property, Location, PropertyImage
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Migrate data from Scrapy to Django database'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true',
                            help='Perform a dry run without making changes')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        if dry_run:
            self.stdout.write(self.style.WARNING('Performing dry run...'))
        else:
            self.stdout.write(self.style.SUCCESS('Starting migration...'))
        migrator = DataMigrator(self.stdout, self.style, dry_run)
        migrator.migrate()


class DataMigrator:
    def __init__(self, stdout, style, dry_run):
        self.stdout = stdout
        self.style = style
        self.dry_run = dry_run
        self.scrapy_conn = psycopg2.connect(
            dbname='database_name',  # Replace with your actual database name
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        self.scrapy_cursor = self.scrapy_conn.cursor()

    def migrate(self):
        try:
            self.scrapy_cursor.execute("SELECT * FROM properties")
            properties = self.scrapy_cursor.fetchall()

            for property_data in properties:
                with transaction.atomic():
                    self.migrate_property(property_data)

            self.stdout.write(self.style.SUCCESS(
                "Successfully migrated all properties"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

        finally:
            self.scrapy_cursor.close()
            self.scrapy_conn.close()

    def migrate_property(self, property_data):
        (id, h3_tag, country_name, city_name, title,
         star, rating, location, latitude, longitude,
         room_type, price, image_paths) = property_data

        if self.dry_run:
            self.stdout.write(f"Would migrate property: {id}")
            return

        property_instance = Property.objects.create(
            property_id=str(id),
            title=title or '',
            description=''
        )

        if country_name:
            country_location, created = Location.objects.get_or_create(
                name__iexact=country_name,
                type='country',
                defaults={
                    'name': country_name,
                    'latitude': latitude,
                    'longitude': longitude
                }
            )
            property_instance.locations.add(country_location)
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Created new country location: {country_name}"))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f"Using existing country location: {country_name}"))

        if city_name:
            city_location, created = Location.objects.get_or_create(
                name__iexact=city_name,
                type='city',
                defaults={
                    'name': city_name,
                    'latitude': latitude,
                    'longitude': longitude
                }
            )
            property_instance.locations.add(city_location)
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Created new city location: {city_name}"))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f"Using existing city location: {city_name}"))

        if image_paths:
            for image_path in image_paths.split(','):
                path_parts = Path(image_path.strip()).parts
                file_name = Path(image_path).name

                full_path = os.path.join(
                    '/home/w3e02/Documents/hello/'
                    'web_crawler/dynamic_crawling/hotel_images',
                    *path_parts
                )

                try:
                    with open(full_path, 'rb') as img_file:
                        django_file = ContentFile(img_file.read())
                        saved_path = default_storage.save(
                            f'property_images/{file_name}', django_file)
                        PropertyImage.objects.create(
                            property=property_instance,
                            image=saved_path,
                            caption=file_name,
                            is_featured=True,
                        )
                except FileNotFoundError:
                    self.stdout.write(self.style.WARNING(
                        f"File not found: {full_path}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"An error occurred: {e}"))

        self.stdout.write(self.style.SUCCESS(
            f"Migrated property: {property_instance.property_id}"))
