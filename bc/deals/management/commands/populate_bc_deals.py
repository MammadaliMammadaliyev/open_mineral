from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from deals.models import (
    BusinessConfirmationDeal, 
    NewBusinessConfirmation, 
    CommercialTerms, 
    PaymentTerms
)
import random


class Command(BaseCommand):
    help = 'Populate business confirmation deals with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing business confirmation deals before populating',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of business confirmation deals to create (default: 5)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing business confirmation deals...')
            BusinessConfirmationDeal.objects.all().delete()

        # Get or create a test user
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created test user: {user}'))

        # Get existing related objects
        new_business_confirmations = list(NewBusinessConfirmation.objects.all())
        commercial_terms_list = list(CommercialTerms.objects.all())
        payment_terms_list = list(PaymentTerms.objects.all())

        if not new_business_confirmations:
            self.stdout.write(
                self.style.ERROR('No NewBusinessConfirmation objects found. Please run populate_new_business_confirmations first.')
            )
            return

        if not commercial_terms_list:
            self.stdout.write(
                self.style.ERROR('No CommercialTerms objects found. Please run populate_commercial_terms first.')
            )
            return

        if not payment_terms_list:
            self.stdout.write(
                self.style.ERROR('No PaymentTerms objects found. Please run populate_payment_terms first.')
            )
            return

        # Status choices
        status_choices = [
            BusinessConfirmationDeal.DRAFT,
            BusinessConfirmationDeal.SUBMITTED,
            BusinessConfirmationDeal.PROCESSING,
            BusinessConfirmationDeal.COMPLETED,
            BusinessConfirmationDeal.CANCELLED
        ]

        created_count = 0
        for i in range(options['count']):
            # Randomly select related objects
            new_business_confirmation = random.choice(new_business_confirmations)
            commercial_terms = random.choice(commercial_terms_list)
            payment_terms = random.choice(payment_terms_list)
            status = random.choice(status_choices)

            # Create business confirmation deal
            bc_deal, created = BusinessConfirmationDeal.objects.get_or_create(
                user=user,
                new_business_confirmation=new_business_confirmation,
                commercial_terms=commercial_terms,
                payment_terms=payment_terms,
                status=status,
                defaults={}
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created business confirmation deal: {bc_deal}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Business confirmation deal already exists: {bc_deal}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} business confirmation deals')
        )
