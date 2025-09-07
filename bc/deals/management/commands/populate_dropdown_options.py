from django.core.management.base import BaseCommand
from deals.models import DropdownOption


class Command(BaseCommand):
    help = 'Populate dropdown options with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing dropdown options before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing dropdown options...')
            DropdownOption.objects.all().delete()

        # Sample dropdown options data
        dropdown_data = [
            {
                'field_name': 'material',
                'option_values': {
                    'akzhal': 'Akzhal',
                    'lead_concentrate': 'Lead Concentrate',
                    'zinc_concentrate': 'Zinc Concentrate',
                    'copper_concentrate': 'Copper Concentrate',
                    'iron_ore': 'Iron Ore',
                    'coal': 'Coal',
                    'gold_concentrate': 'Gold Concentrate',
                    'silver_concentrate': 'Silver Concentrate'
                },
                'display_order': 1,
                'tooltip_text': 'Select the type of mineral material for this deal',
                'is_active': True
            },
            {
                'field_name': 'delivery_term',
                'option_values': {
                    'dap': 'DAP (Delivered at Place)',
                    'fob': 'FOB (Free on Board)',
                    'cif': 'CIF (Cost, Insurance, Freight)',
                    'exw': 'EXW (Ex Works)',
                    'fca': 'FCA (Free Carrier)',
                    'cpt': 'CPT (Carriage Paid To)',
                    'cip': 'CIP (Carriage and Insurance Paid To)',
                    'ddp': 'DDP (Delivered Duty Paid)'
                },
                'display_order': 2,
                'tooltip_text': 'Choose the delivery term that defines when risk and responsibility transfer',
                'is_active': True
            },
            {
                'field_name': 'packaging',
                'option_values': {
                    'big_bags': 'Big Bags',
                    'bulk': 'Bulk',
                    'containers': 'Containers',
                    'drums': 'Drums',
                    'pallets': 'Pallets',
                    'sacks': 'Sacks',
                    'totes': 'Totes'
                },
                'display_order': 3,
                'tooltip_text': 'Select the packaging type for the material',
                'is_active': True
            },
            {
                'field_name': 'transport_mode',
                'option_values': {
                    'rail': 'Rail',
                    'ship': 'Ship',
                    'truck': 'Truck',
                    'air': 'Air',
                    'pipeline': 'Pipeline',
                    'barge': 'Barge',
                    'multimodal': 'Multimodal'
                },
                'display_order': 4,
                'tooltip_text': 'Choose the primary transport mode for delivery',
                'is_active': True
            },
            {
                'field_name': 'payment_method',
                'option_values': {
                    'tt': 'T/T (Telegraphic Transfer)',
                    'lc': 'L/C (Letter of Credit)',
                    'bank_guarantee': 'Bank Guarantee',
                    'cash': 'Cash',
                    'check': 'Check',
                    'wire_transfer': 'Wire Transfer',
                    'escrow': 'Escrow'
                },
                'display_order': 5,
                'tooltip_text': 'Select the payment method for this transaction',
                'is_active': True
            },
            {
                'field_name': 'currency',
                'option_values': {
                    'usd': 'USD (US Dollar)',
                    'eur': 'EUR (Euro)',
                    'gbp': 'GBP (British Pound)',
                    'cny': 'CNY (Chinese Yuan)',
                    'jpy': 'JPY (Japanese Yen)',
                    'cad': 'CAD (Canadian Dollar)',
                    'aud': 'AUD (Australian Dollar)',
                    'chf': 'CHF (Swiss Franc)'
                },
                'display_order': 6,
                'tooltip_text': 'Choose the currency for pricing and payment',
                'is_active': True
            },
            {
                'field_name': 'treatment_charge_unit',
                'option_values': {
                    'dmt': 'DMT (Dry Metric Ton)',
                    'mt': 'MT (Metric Ton)',
                    'lb': 'LB (Pound)',
                    'oz': 'OZ (Ounce)',
                    'kg': 'KG (Kilogram)',
                    'ton': 'TON (Ton)'
                },
                'display_order': 7,
                'tooltip_text': 'Unit of measurement for treatment charges',
                'is_active': True
            },
            {
                'field_name': 'refining_charge_unit',
                'option_values': {
                    'toz': 'TOZ (Troy Ounce)',
                    'oz': 'OZ (Ounce)',
                    'kg': 'KG (Kilogram)',
                    'g': 'G (Gram)',
                    'lb': 'LB (Pound)',
                    'dmt': 'DMT (Dry Metric Ton)'
                },
                'display_order': 8,
                'tooltip_text': 'Unit of measurement for refining charges',
                'is_active': True
            }
        ]

        created_count = 0
        for data in dropdown_data:
            dropdown_option, created = DropdownOption.objects.get_or_create(
                field_name=data['field_name'],
                option_values=data['option_values'],
                defaults={
                    'display_order': data['display_order'],
                    'tooltip_text': data['tooltip_text'],
                    'is_active': data['is_active']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created dropdown option: {dropdown_option}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Dropdown option already exists: {dropdown_option}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} dropdown options')
        )
