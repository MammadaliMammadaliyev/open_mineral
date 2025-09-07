from django.core.management.base import BaseCommand
from deals.models import NewBusinessConfirmation
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate new business confirmations with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing new business confirmations before populating',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of new business confirmations to create (default: 10)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing new business confirmations...')
            NewBusinessConfirmation.objects.all().delete()

        # Sample new business confirmations data
        business_data = [
            {
                'seller': 'Open Mineral',
                'buyer': 'ABC Mining Corp',
                'material': 'Lead Concentrate',
                'quantity': Decimal('500.00')
            },
            {
                'seller': 'Open Mineral',
                'buyer': 'Global Metals Ltd',
                'material': 'Zinc Concentrate',
                'quantity': Decimal('750.50')
            },
            {
                'seller': 'Open Mineral',
                'buyer': 'Industrial Minerals Inc',
                'material': 'Copper Concentrate',
                'quantity': Decimal('1000.25')
            },
            {
                'seller': 'Open Mineral',
                'buyer': 'Steel Manufacturing Co',
                'material': 'Iron Ore',
                'quantity': Decimal('2000.00')
            },
            {
                'seller': 'Open Mineral',
                'buyer': 'Energy Solutions Ltd',
                'material': 'Coal',
                'quantity': Decimal('1500.75')
            },
            {
                'seller': 'Open Mineral',
                'buyer': 'Precious Metals Group',
                'material': 'Gold Concentrate',
                'quantity': Decimal('25.30')
            },
            {
                'seller': 'Open Mineral',
                'buyer': 'Silver Trading Corp',
                'material': 'Silver Concentrate',
                'quantity': Decimal('100.00')
            },
            {
                'seller': 'Open Mineral',
                'buyer': 'Mining Ventures LLC',
                'material': 'Akzhal',
                'quantity': Decimal('300.00')
            },
            {
                'seller': 'Open Mineral',
                'buyer': 'International Minerals',
                'material': 'Lead Concentrate',
                'quantity': Decimal('800.50')
            },
            {
                'seller': 'Open Mineral',
                'buyer': 'Commodity Traders Ltd',
                'material': 'Zinc Concentrate',
                'quantity': Decimal('1200.25')
            },
            {
                'seller': 'Open Mineral',
                'buyer': 'Metals Processing Co',
                'material': 'Copper Concentrate',
                'quantity': Decimal('600.00')
            },
            {
                'seller': 'Open Mineral',
                'buyer': 'Steel Works Inc',
                'material': 'Iron Ore',
                'quantity': Decimal('3000.00')
            },
            {
                'seller': 'Open Mineral',
                'buyer': 'Power Generation Ltd',
                'material': 'Coal',
                'quantity': Decimal('2500.50')
            },
            {
                'seller': 'Open Mineral',
                'buyer': 'Gold Refiners Corp',
                'material': 'Gold Concentrate',
                'quantity': Decimal('50.75')
            },
            {
                'seller': 'Open Mineral',
                'buyer': 'Silver Refining Ltd',
                'material': 'Silver Concentrate',
                'quantity': Decimal('200.00')
            }
        ]

        # Limit the number of records to create
        count = min(options['count'], len(business_data))
        business_data = business_data[:count]

        created_count = 0
        for data in business_data:
            business_confirmation, created = NewBusinessConfirmation.objects.get_or_create(
                seller=data['seller'],
                buyer=data['buyer'],
                material=data['material'],
                quantity=data['quantity'],
                defaults={}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created new business confirmation: {business_confirmation}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'New business confirmation already exists: {business_confirmation}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new business confirmations')
        )
