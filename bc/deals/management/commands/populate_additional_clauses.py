from django.core.management.base import BaseCommand
from deals.models import AdditionalClause


class Command(BaseCommand):
    help = 'Populate additional clauses with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing additional clauses before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing additional clauses...')
            AdditionalClause.objects.all().delete()

        # Sample additional clauses data
        clauses_data = [
            {
                'clause': 'The material shall be delivered in accordance with the specifications provided in the assay certificate.',
                'display_order': 1
            },
            {
                'clause': 'All costs and risks of the material shall pass to the buyer upon delivery at the agreed delivery point.',
                'display_order': 2
            },
            {
                'clause': 'The seller warrants that the material is free from any liens, encumbrances, or third-party claims.',
                'display_order': 3
            },
            {
                'clause': 'Any disputes arising from this agreement shall be resolved through arbitration in accordance with the rules of the International Chamber of Commerce.',
                'display_order': 4
            },
            {
                'clause': 'The buyer shall have the right to inspect the material within 48 hours of delivery and may reject any material that does not meet specifications.',
                'display_order': 5
            },
            {
                'clause': 'Force majeure events including but not limited to natural disasters, war, or government actions shall excuse performance delays.',
                'display_order': 6
            },
            {
                'clause': 'All payments shall be made in the agreed currency and are due within 30 days of invoice date unless otherwise specified.',
                'display_order': 7
            },
            {
                'clause': 'The seller shall provide all necessary documentation including certificates of origin, quality certificates, and shipping documents.',
                'display_order': 8
            },
            {
                'clause': 'This agreement shall be governed by the laws of the jurisdiction specified in the commercial terms.',
                'display_order': 9
            },
            {
                'clause': 'Any modifications to this agreement must be made in writing and signed by both parties.',
                'display_order': 10
            },
            {
                'clause': 'The material shall comply with all applicable environmental and safety regulations in both origin and destination countries.',
                'display_order': 11
            },
            {
                'clause': 'Insurance coverage shall be maintained by the seller until delivery and by the buyer thereafter.',
                'display_order': 12
            },
            {
                'clause': 'Sampling and analysis shall be conducted by an independent third-party laboratory agreed upon by both parties.',
                'display_order': 13
            },
            {
                'clause': 'The buyer shall have the right to assign this agreement to an affiliate with prior written consent from the seller.',
                'display_order': 14
            },
            {
                'clause': 'All confidential information exchanged between the parties shall remain confidential and shall not be disclosed to third parties.',
                'display_order': 15
            }
        ]

        created_count = 0
        for data in clauses_data:
            clause, created = AdditionalClause.objects.get_or_create(
                clause=data['clause'],
                defaults={
                    'display_order': data['display_order']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created additional clause: {clause}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Additional clause already exists: {clause}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} additional clauses')
        )
