from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Populate all models with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of records to create for each model (default: 10)',
        )

    def handle(self, *args, **options):
        clear_flag = '--clear' if options['clear'] else ''
        count = options['count']

        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Run commands in dependency order
        commands = [
            ('populate_dropdown_options', 'Populating dropdown options...'),
            ('populate_additional_clauses', 'Populating additional clauses...'),
            ('populate_new_business_confirmations', 'Populating new business confirmations...'),
            ('populate_commercial_terms', 'Populating commercial terms...'),
            ('populate_payment_terms', 'Populating payment terms...'),
            ('populate_bc_deals', 'Populating business confirmation deals...'),
        ]

        for command_name, description in commands:
            self.stdout.write(f'{description}')
            try:
                if clear_flag and command_name in ['populate_dropdown_options', 'populate_additional_clauses']:
                    call_command(command_name, clear_flag)
                elif command_name == 'populate_bc_deals':
                    # BC deals need fewer records as they combine other models
                    call_command(command_name, clear_flag, count=min(count, 5))
                else:
                    call_command(command_name, clear_flag, count=count)
                self.stdout.write(self.style.SUCCESS(f'✓ {description} completed'))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ {description} failed: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS('Database population completed!')
        )
