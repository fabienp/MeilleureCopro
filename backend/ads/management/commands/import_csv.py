import csv
from django.core.management.base import BaseCommand
from ads.models import RealEstateAd

class Command(BaseCommand):
    help = 'Import RealEstateAd from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                # Extraire bienici_id depuis l'URL
                ad_url = row.get('AD_URLS', '').strip()
                if not ad_url:
                    continue
                bienici_id = ad_url.rstrip('/').split('/')[-1]

                # condo_fees = float si possible, sinon 0
                try:
                    condo_fees = float(row.get('CONDOMINIUM_EXPENSES', 0) or 0)
                except ValueError:
                    condo_fees = 0

                # Créer ou ignorer si déjà présent
                obj, created = RealEstateAd.objects.get_or_create(
                    bienici_id=bienici_id,
                    defaults={
                        'condo_fees': condo_fees,
                        'department': row.get('DEPT_CODE', '').strip(),
                        'postal_code': row.get('ZIP_CODE', '').strip(),
                        'city': row.get('CITY', '').strip(),
                    }
                )

                if created:
                    count += 1

            self.stdout.write(self.style.SUCCESS(f'Imported {count} ads'))
