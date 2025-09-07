from django.core.management.base import BaseCommand
from deals.models import CommercialTerms
from decimal import Decimal
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate commercial terms with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing commercial terms before populating',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of commercial terms to create (default: 10)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing commercial terms...')
            CommercialTerms.objects.all().delete()

        # Sample commercial terms data
        commercial_terms_data = [
            {
                'delivery_term': 'DAP',
                'delivery_point': 'Shanghai Port, China',
                'packaging': 'Big Bags',
                'transport_mode': 'Ship',
                'inland_freight_buyer': True,
                'shipment_start_date': date.today() + timedelta(days=30),
                'shipment_end_date': date.today() + timedelta(days=60),
                'shipment_evenly_distributed': True,
                'treatment_charge': Decimal('150.00'),
                'treatment_charge_unit': 'dmt',
                'refining_charge': Decimal('0.25'),
                'refining_charge_unit': 'toz',
                'china_import_compliant': True,
                'clauses': ['Material must meet LME specifications', 'Sampling by independent surveyor']
            },
            {
                'delivery_term': 'FOB',
                'delivery_point': 'Hamburg Port, Germany',
                'packaging': 'Bulk',
                'transport_mode': 'Ship',
                'inland_freight_buyer': False,
                'shipment_start_date': date.today() + timedelta(days=45),
                'shipment_end_date': date.today() + timedelta(days=75),
                'shipment_evenly_distributed': False,
                'treatment_charge': Decimal('200.00'),
                'treatment_charge_unit': 'dmt',
                'refining_charge': Decimal('0.30'),
                'refining_charge_unit': 'toz',
                'china_import_compliant': False,
                'clauses': ['Quality based on seller\'s analysis', 'Payment within 30 days']
            },
            {
                'delivery_term': 'CIF',
                'delivery_point': 'Los Angeles Port, USA',
                'packaging': 'Containers',
                'transport_mode': 'Ship',
                'inland_freight_buyer': False,
                'shipment_start_date': date.today() + timedelta(days=20),
                'shipment_end_date': date.today() + timedelta(days=50),
                'shipment_evenly_distributed': True,
                'treatment_charge': Decimal('175.00'),
                'treatment_charge_unit': 'dmt',
                'refining_charge': Decimal('0.28'),
                'refining_charge_unit': 'toz',
                'china_import_compliant': True,
                'clauses': ['Insurance included in price', 'Delivery within agreed timeframe']
            },
            {
                'delivery_term': 'EXW',
                'delivery_point': 'Mine Site, Kazakhstan',
                'packaging': 'Big Bags',
                'transport_mode': 'Rail',
                'inland_freight_buyer': True,
                'shipment_start_date': date.today() + timedelta(days=15),
                'shipment_end_date': date.today() + timedelta(days=45),
                'shipment_evenly_distributed': False,
                'treatment_charge': Decimal('100.00'),
                'treatment_charge_unit': 'dmt',
                'refining_charge': Decimal('0.20'),
                'refining_charge_unit': 'toz',
                'china_import_compliant': True,
                'clauses': ['Buyer responsible for all transport', 'Quality as per mine specifications']
            },
            {
                'delivery_term': 'DDP',
                'delivery_point': 'Buyer\'s Warehouse, Japan',
                'packaging': 'Drums',
                'transport_mode': 'Multimodal',
                'inland_freight_buyer': False,
                'shipment_start_date': date.today() + timedelta(days=60),
                'shipment_end_date': date.today() + timedelta(days=90),
                'shipment_evenly_distributed': True,
                'treatment_charge': Decimal('250.00'),
                'treatment_charge_unit': 'dmt',
                'refining_charge': Decimal('0.35'),
                'refining_charge_unit': 'toz',
                'china_import_compliant': True,
                'clauses': ['All duties and taxes included', 'Delivery to final destination']
            },
            {
                'delivery_term': 'FCA',
                'delivery_point': 'Rail Terminal, Russia',
                'packaging': 'Bulk',
                'transport_mode': 'Rail',
                'inland_freight_buyer': True,
                'shipment_start_date': date.today() + timedelta(days=25),
                'shipment_end_date': date.today() + timedelta(days=55),
                'shipment_evenly_distributed': True,
                'treatment_charge': Decimal('125.00'),
                'treatment_charge_unit': 'dmt',
                'refining_charge': Decimal('0.22'),
                'refining_charge_unit': 'toz',
                'china_import_compliant': False,
                'clauses': ['Risk transfers at terminal', 'Buyer arranges onward transport']
            },
            {
                'delivery_term': 'CPT',
                'delivery_point': 'Port of Rotterdam, Netherlands',
                'packaging': 'Big Bags',
                'transport_mode': 'Ship',
                'inland_freight_buyer': False,
                'shipment_start_date': date.today() + timedelta(days=40),
                'shipment_end_date': date.today() + timedelta(days=70),
                'shipment_evenly_distributed': False,
                'treatment_charge': Decimal('180.00'),
                'treatment_charge_unit': 'dmt',
                'refining_charge': Decimal('0.26'),
                'refining_charge_unit': 'toz',
                'china_import_compliant': True,
                'clauses': ['Carriage paid to destination', 'Risk transfers on delivery']
            },
            {
                'delivery_term': 'CIP',
                'delivery_point': 'Port of Antwerp, Belgium',
                'packaging': 'Containers',
                'transport_mode': 'Ship',
                'inland_freight_buyer': False,
                'shipment_start_date': date.today() + timedelta(days=35),
                'shipment_end_date': date.today() + timedelta(days=65),
                'shipment_evenly_distributed': True,
                'treatment_charge': Decimal('190.00'),
                'treatment_charge_unit': 'dmt',
                'refining_charge': Decimal('0.27'),
                'refining_charge_unit': 'toz',
                'china_import_compliant': True,
                'clauses': ['Insurance and carriage included', 'Quality based on final destination analysis']
            },
            {
                'delivery_term': 'DAP',
                'delivery_point': 'Mumbai Port, India',
                'packaging': 'Bulk',
                'transport_mode': 'Ship',
                'inland_freight_buyer': True,
                'shipment_start_date': date.today() + timedelta(days=50),
                'shipment_end_date': date.today() + timedelta(days=80),
                'shipment_evenly_distributed': False,
                'treatment_charge': Decimal('160.00'),
                'treatment_charge_unit': 'dmt',
                'refining_charge': Decimal('0.24'),
                'refining_charge_unit': 'toz',
                'china_import_compliant': False,
                'clauses': ['Delivered at place', 'Buyer responsible for import clearance']
            },
            {
                'delivery_term': 'FOB',
                'delivery_point': 'Port of Santos, Brazil',
                'packaging': 'Big Bags',
                'transport_mode': 'Ship',
                'inland_freight_buyer': False,
                'shipment_start_date': date.today() + timedelta(days=55),
                'shipment_end_date': date.today() + timedelta(days=85),
                'shipment_evenly_distributed': True,
                'treatment_charge': Decimal('170.00'),
                'treatment_charge_unit': 'dmt',
                'refining_charge': Decimal('0.25'),
                'refining_charge_unit': 'toz',
                'china_import_compliant': True,
                'clauses': ['Free on board vessel', 'Quality as per loading port analysis']
            }
        ]

        # Limit the number of records to create
        count = min(options['count'], len(commercial_terms_data))
        commercial_terms_data = commercial_terms_data[:count]

        created_count = 0
        for data in commercial_terms_data:
            commercial_terms, created = CommercialTerms.objects.get_or_create(
                delivery_term=data['delivery_term'],
                delivery_point=data['delivery_point'],
                packaging=data['packaging'],
                transport_mode=data['transport_mode'],
                defaults={
                    'inland_freight_buyer': data['inland_freight_buyer'],
                    'shipment_start_date': data['shipment_start_date'],
                    'shipment_end_date': data['shipment_end_date'],
                    'shipment_evenly_distributed': data['shipment_evenly_distributed'],
                    'treatment_charge': data['treatment_charge'],
                    'treatment_charge_unit': data['treatment_charge_unit'],
                    'refining_charge': data['refining_charge'],
                    'refining_charge_unit': data['refining_charge_unit'],
                    'china_import_compliant': data['china_import_compliant'],
                    'clauses': data['clauses']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created commercial terms: {commercial_terms}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Commercial terms already exists: {commercial_terms}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} commercial terms')
        )
