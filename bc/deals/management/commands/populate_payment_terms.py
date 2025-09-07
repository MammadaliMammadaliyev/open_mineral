from django.core.management.base import BaseCommand
from deals.models import PaymentTerms
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate payment terms with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing payment terms before populating',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of payment terms to create (default: 10)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing payment terms...')
            PaymentTerms.objects.all().delete()

        # Sample payment terms data
        payment_terms_data = [
            {
                'prepayment_percentage': Decimal('20.00'),
                'prepayment_trigger': 'Upon signing of contract',
                'provisional_payment_terms': 'Payment within 30 days of provisional invoice based on estimated weights and assays',
                'final_payment_terms': 'Final payment within 10 days of final invoice with final weights and assays',
                'payment_method': 'T/T (Telegraphic Transfer)',
                'currency': 'USD',
                'triggering_event': 'Delivery of material to buyer',
                'reference_document': 'Commercial Invoice',
                'final_determination_location': 'Loading Port',
                'buyer_cost_share_percentage': Decimal('50.00'),
                'seller_cost_share_percentage': Decimal('50.00'),
                'nominated_by': 'Buyer',
                'agreed_by': 'Seller',
                'surveyor_notes': 'Independent surveyor to be appointed by mutual agreement'
            },
            {
                'prepayment_percentage': Decimal('30.00'),
                'prepayment_trigger': 'Upon receipt of shipping documents',
                'provisional_payment_terms': 'Payment within 15 days of provisional invoice',
                'final_payment_terms': 'Final payment within 5 days of final invoice',
                'payment_method': 'L/C (Letter of Credit)',
                'currency': 'EUR',
                'triggering_event': 'Presentation of documents',
                'reference_document': 'Bill of Lading',
                'final_determination_location': 'Discharge Port',
                'buyer_cost_share_percentage': Decimal('60.00'),
                'seller_cost_share_percentage': Decimal('40.00'),
                'nominated_by': 'Seller',
                'agreed_by': 'Buyer',
                'surveyor_notes': 'Surveyor to be from approved list provided by both parties'
            },
            {
                'prepayment_percentage': Decimal('10.00'),
                'prepayment_trigger': 'Upon contract execution',
                'provisional_payment_terms': 'Payment within 45 days of provisional invoice',
                'final_payment_terms': 'Final payment within 15 days of final invoice',
                'payment_method': 'Bank Guarantee',
                'currency': 'GBP',
                'triggering_event': 'Material delivery confirmation',
                'reference_document': 'Delivery Receipt',
                'final_determination_location': 'Buyer\'s Warehouse',
                'buyer_cost_share_percentage': Decimal('40.00'),
                'seller_cost_share_percentage': Decimal('60.00'),
                'nominated_by': 'Buyer',
                'agreed_by': 'Seller',
                'surveyor_notes': 'Surveyor must be certified and independent'
            },
            {
                'prepayment_percentage': Decimal('25.00'),
                'prepayment_trigger': 'Upon receipt of proforma invoice',
                'provisional_payment_terms': 'Payment within 20 days of provisional invoice',
                'final_payment_terms': 'Final payment within 7 days of final invoice',
                'payment_method': 'T/T (Telegraphic Transfer)',
                'currency': 'CNY',
                'triggering_event': 'Vessel departure from loading port',
                'reference_document': 'Certificate of Origin',
                'final_determination_location': 'Loading Port',
                'buyer_cost_share_percentage': Decimal('50.00'),
                'seller_cost_share_percentage': Decimal('50.00'),
                'nominated_by': 'Seller',
                'agreed_by': 'Buyer',
                'surveyor_notes': 'Surveyor to be appointed from SGS, Bureau Veritas, or similar'
            },
            {
                'prepayment_percentage': Decimal('15.00'),
                'prepayment_trigger': 'Upon contract signing and bank guarantee',
                'provisional_payment_terms': 'Payment within 30 days of provisional invoice',
                'final_payment_terms': 'Final payment within 12 days of final invoice',
                'payment_method': 'Escrow',
                'currency': 'USD',
                'triggering_event': 'Material acceptance by buyer',
                'reference_document': 'Quality Certificate',
                'final_determination_location': 'Discharge Port',
                'buyer_cost_share_percentage': Decimal('55.00'),
                'seller_cost_share_percentage': Decimal('45.00'),
                'nominated_by': 'Buyer',
                'agreed_by': 'Seller',
                'surveyor_notes': 'Surveyor to be mutually agreed and costs shared equally'
            },
            {
                'prepayment_percentage': Decimal('35.00'),
                'prepayment_trigger': 'Upon receipt of shipping documents',
                'provisional_payment_terms': 'Payment within 10 days of provisional invoice',
                'final_payment_terms': 'Final payment within 3 days of final invoice',
                'payment_method': 'L/C (Letter of Credit)',
                'currency': 'JPY',
                'triggering_event': 'Document presentation',
                'reference_document': 'Insurance Certificate',
                'final_determination_location': 'Loading Port',
                'buyer_cost_share_percentage': Decimal('45.00'),
                'seller_cost_share_percentage': Decimal('55.00'),
                'nominated_by': 'Seller',
                'agreed_by': 'Buyer',
                'surveyor_notes': 'Surveyor must be from approved international list'
            },
            {
                'prepayment_percentage': Decimal('5.00'),
                'prepayment_trigger': 'Upon contract execution',
                'provisional_payment_terms': 'Payment within 60 days of provisional invoice',
                'final_payment_terms': 'Final payment within 20 days of final invoice',
                'payment_method': 'T/T (Telegraphic Transfer)',
                'currency': 'CAD',
                'triggering_event': 'Material delivery and acceptance',
                'reference_document': 'Delivery Note',
                'final_determination_location': 'Buyer\'s Facility',
                'buyer_cost_share_percentage': Decimal('60.00'),
                'seller_cost_share_percentage': Decimal('40.00'),
                'nominated_by': 'Buyer',
                'agreed_by': 'Seller',
                'surveyor_notes': 'Surveyor to be appointed by buyer with seller approval'
            },
            {
                'prepayment_percentage': Decimal('40.00'),
                'prepayment_trigger': 'Upon receipt of shipping documents',
                'provisional_payment_terms': 'Payment within 7 days of provisional invoice',
                'final_payment_terms': 'Final payment within 2 days of final invoice',
                'payment_method': 'Wire Transfer',
                'currency': 'AUD',
                'triggering_event': 'Vessel loading completion',
                'reference_document': 'Mate\'s Receipt',
                'final_determination_location': 'Discharge Port',
                'buyer_cost_share_percentage': Decimal('50.00'),
                'seller_cost_share_percentage': Decimal('50.00'),
                'nominated_by': 'Seller',
                'agreed_by': 'Buyer',
                'surveyor_notes': 'Surveyor to be from internationally recognized organization'
            },
            {
                'prepayment_percentage': Decimal('12.00'),
                'prepayment_trigger': 'Upon contract signing',
                'provisional_payment_terms': 'Payment within 25 days of provisional invoice',
                'final_payment_terms': 'Final payment within 8 days of final invoice',
                'payment_method': 'Bank Guarantee',
                'currency': 'CHF',
                'triggering_event': 'Material arrival at destination',
                'reference_document': 'Warehouse Receipt',
                'final_determination_location': 'Loading Port',
                'buyer_cost_share_percentage': Decimal('48.00'),
                'seller_cost_share_percentage': Decimal('52.00'),
                'nominated_by': 'Buyer',
                'agreed_by': 'Seller',
                'surveyor_notes': 'Surveyor to be mutually agreed and costs shared proportionally'
            },
            {
                'prepayment_percentage': Decimal('22.00'),
                'prepayment_trigger': 'Upon receipt of proforma invoice',
                'provisional_payment_terms': 'Payment within 18 days of provisional invoice',
                'final_payment_terms': 'Final payment within 6 days of final invoice',
                'payment_method': 'T/T (Telegraphic Transfer)',
                'currency': 'USD',
                'triggering_event': 'Bill of lading date',
                'reference_document': 'Packing List',
                'final_determination_location': 'Discharge Port',
                'buyer_cost_share_percentage': Decimal('52.00'),
                'seller_cost_share_percentage': Decimal('48.00'),
                'nominated_by': 'Seller',
                'agreed_by': 'Buyer',
                'surveyor_notes': 'Surveyor to be from approved list of international surveyors'
            }
        ]

        # Limit the number of records to create
        count = min(options['count'], len(payment_terms_data))
        payment_terms_data = payment_terms_data[:count]

        created_count = 0
        for data in payment_terms_data:
            payment_terms, created = PaymentTerms.objects.get_or_create(
                payment_method=data['payment_method'],
                currency=data['currency'],
                prepayment_percentage=data['prepayment_percentage'],
                defaults={
                    'prepayment_trigger': data['prepayment_trigger'],
                    'provisional_payment_terms': data['provisional_payment_terms'],
                    'final_payment_terms': data['final_payment_terms'],
                    'triggering_event': data['triggering_event'],
                    'reference_document': data['reference_document'],
                    'final_determination_location': data['final_determination_location'],
                    'buyer_cost_share_percentage': data['buyer_cost_share_percentage'],
                    'seller_cost_share_percentage': data['seller_cost_share_percentage'],
                    'nominated_by': data['nominated_by'],
                    'agreed_by': data['agreed_by'],
                    'surveyor_notes': data['surveyor_notes']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created payment terms: {payment_terms}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Payment terms already exists: {payment_terms}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} payment terms')
        )
