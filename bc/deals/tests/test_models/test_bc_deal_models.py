import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from deals.models import (
    NewBusinessConfirmation, BusinessConfirmationDeal,
    CommercialTerms, PaymentTerms, DropdownOption,
    AdditionalClause, TaskStatus
)
from deals.tests.factories import (
    UserFactory, NewBusinessConfirmationFactory,
    CommercialTermsFactory, PaymentTermsFactory,
    BusinessConfirmationDealFactory, TaskStatusFactory
)

User = get_user_model()


@pytest.mark.django_db
class TestNewBusinessConfirmation:
    """Test cases for NewBusinessConfirmation model"""

    def test_create_new_business_confirmation(self):
        """Test creating a new business confirmation with valid data"""
        confirmation = NewBusinessConfirmationFactory(
            seller="Open Mineral",
            buyer="Test Company",
            material="Akzhal",
            quantity=Decimal('1000.50')
        )
        
        assert confirmation.seller == "Open Mineral"
        assert confirmation.buyer == "Test Company"
        assert confirmation.material == "Akzhal"
        assert confirmation.quantity == Decimal('1000.50')
        assert confirmation.created_at is not None
        assert confirmation.updated_at is not None

    def test_string_representation(self):
        """Test string representation of NewBusinessConfirmation"""
        confirmation = NewBusinessConfirmationFactory(
            buyer="Test Company",
            material="Lead concentrate"
        )
        
        expected = f"New Business Confirmation {confirmation.id}: Test Company - Lead concentrate"
        assert str(confirmation) == expected

    def test_quantity_validation(self):
        """Test quantity validation with minimum value"""
        with pytest.raises(ValidationError):
            confirmation = NewBusinessConfirmationFactory.build(quantity=Decimal('0.00'))
            confirmation.full_clean()

    def test_quantity_negative_validation(self):
        """Test quantity validation with negative value"""
        with pytest.raises(ValidationError):
            confirmation = NewBusinessConfirmationFactory.build(quantity=Decimal('-100.00'))
            confirmation.full_clean()

    def test_ordering(self):
        """Test that confirmations are ordered by created_at descending"""
        confirmation1 = NewBusinessConfirmationFactory()
        confirmation2 = NewBusinessConfirmationFactory()
        
        confirmations = NewBusinessConfirmation.objects.all()
        assert confirmations[0] == confirmation2  # Most recent first
        assert confirmations[1] == confirmation1


@pytest.mark.django_db
class TestBusinessConfirmationDeal:
    """Test cases for BusinessConfirmationDeal model"""

    def test_create_business_confirmation_deal(self):
        """Test creating a business confirmation deal with all relationships"""
        user = UserFactory()
        confirmation = NewBusinessConfirmationFactory()
        commercial_terms = CommercialTermsFactory()
        payment_terms = PaymentTermsFactory()
        
        deal = BusinessConfirmationDeal.objects.create(
            user=user,
            new_business_confirmation=confirmation,
            commercial_terms=commercial_terms,
            payment_terms=payment_terms,
            status=BusinessConfirmationDeal.DRAFT
        )
        
        assert deal.user == user
        assert deal.new_business_confirmation == confirmation
        assert deal.commercial_terms == commercial_terms
        assert deal.payment_terms == payment_terms
        assert deal.status == BusinessConfirmationDeal.DRAFT
        assert deal.created_at is not None
        assert deal.updated_at is not None

    def test_deal_status_choices(self):
        """Test that deal status is limited to valid choices"""
        deal = BusinessConfirmationDealFactory(status=BusinessConfirmationDeal.DRAFT)
        assert deal.status in [choice[0] for choice in BusinessConfirmationDeal.STATUS_CHOICES]

    def test_deal_string_representation(self):
        """Test string representation of BusinessConfirmationDeal"""
        deal = BusinessConfirmationDealFactory()
        expected = f"Business Confirmation Deal {deal.id}"
        assert str(deal) == expected

    def test_deal_without_optional_fields(self):
        """Test creating deal without optional fields"""
        deal = BusinessConfirmationDeal.objects.create(status=BusinessConfirmationDeal.DRAFT)
        
        assert deal.user is None
        assert deal.new_business_confirmation is None
        assert deal.commercial_terms is None
        assert deal.payment_terms is None
        assert deal.status == BusinessConfirmationDeal.DRAFT

    def test_deal_status_transitions(self):
        """Test valid status transitions"""
        deal = BusinessConfirmationDealFactory(status=BusinessConfirmationDeal.DRAFT)
        
        deal.status = BusinessConfirmationDeal.SUBMITTED
        deal.save()
        assert deal.status == BusinessConfirmationDeal.SUBMITTED
        
        deal.status = BusinessConfirmationDeal.PROCESSING
        deal.save()
        assert deal.status == BusinessConfirmationDeal.PROCESSING
        
        deal.status = BusinessConfirmationDeal.COMPLETED
        deal.save()
        assert deal.status == BusinessConfirmationDeal.COMPLETED


@pytest.mark.django_db
class TestCommercialTerms:
    """Test cases for CommercialTerms model"""

    def test_create_commercial_terms(self):
        """Test creating commercial terms with all fields"""
        terms = CommercialTermsFactory(
            delivery_term='DAP',
            delivery_point='Port of Rotterdam',
            packaging='Big Bags',
            transport_mode='Ship',
            inland_freight_buyer=True,
            treatment_charge=Decimal('75.50'),
            refining_charge=Decimal('45.25')
        )
        
        assert terms.delivery_term == 'DAP'
        assert terms.delivery_point == 'Port of Rotterdam'
        assert terms.packaging == 'Big Bags'
        assert terms.transport_mode == 'Ship'
        assert terms.inland_freight_buyer is True
        assert terms.treatment_charge == Decimal('75.50')
        assert terms.refining_charge == Decimal('45.25')

    def test_charge_validation_negative_values(self):
        """Test that charges cannot be negative"""
        with pytest.raises(ValidationError):
            terms = CommercialTermsFactory.build(treatment_charge=Decimal('-10.00'))
            terms.full_clean()

    def test_shipment_date_validation(self):
        """Test shipment date validation"""
        terms = CommercialTermsFactory(
            shipment_start_date='2024-01-01',
            shipment_end_date='2024-01-31'
        )
        
        assert terms.shipment_start_date < terms.shipment_end_date

    def test_charge_units_default(self):
        """Test default charge units"""
        terms = CommercialTermsFactory()
        assert terms.treatment_charge_unit == 'dmt'
        assert terms.refining_charge_unit == 'dmt'


@pytest.mark.django_db
class TestPaymentTerms:
    """Test cases for PaymentTerms model"""

    def test_create_payment_terms(self):
        """Test creating payment terms with all stages"""
        terms = PaymentTermsFactory(
            payment_stage_1_percentage=Decimal('30.00'),
            payment_stage_1_days=30,
            payment_stage_2_percentage=Decimal('40.00'),
            payment_stage_2_days=60,
            payment_stage_3_percentage=Decimal('30.00'),
            payment_stage_3_days=90,
            currency='USD',
            payment_method='Bank Transfer'
        )
        
        assert terms.payment_stage_1_percentage == Decimal('30.00')
        assert terms.payment_stage_1_days == 30
        assert terms.payment_stage_2_percentage == Decimal('40.00')
        assert terms.payment_stage_2_days == 60
        assert terms.payment_stage_3_percentage == Decimal('30.00')
        assert terms.payment_stage_3_days == 90
        assert terms.currency == 'USD'
        assert terms.payment_method == 'Bank Transfer'

    def test_payment_percentages_sum_validation(self):
        """Test that payment percentages sum to 100%"""
        terms = PaymentTermsFactory(
            payment_stage_1_percentage=Decimal('30.00'),
            payment_stage_2_percentage=Decimal('40.00'),
            payment_stage_3_percentage=Decimal('30.00')
        )
        
        total = (terms.payment_stage_1_percentage + 
                terms.payment_stage_2_percentage + 
                terms.payment_stage_3_percentage)
        assert total == Decimal('100.00')

    def test_negative_payment_percentage_validation(self):
        """Test that payment percentages cannot be negative"""
        with pytest.raises(ValidationError):
            terms = PaymentTermsFactory.build(payment_stage_1_percentage=Decimal('-10.00'))
            terms.full_clean()

    def test_credit_terms_validation(self):
        """Test credit terms validation"""
        terms = PaymentTermsFactory(credit_terms_days=30)
        assert terms.credit_terms_days == 30
        
        with pytest.raises(ValidationError):
            terms = PaymentTermsFactory.build(credit_terms_days=-5)
            terms.full_clean()


@pytest.mark.django_db
class TestTaskStatus:
    """Test cases for TaskStatus model"""

    def test_create_task_status(self):
        """Test creating task status with all fields"""
        deal = BusinessConfirmationDealFactory()
        task_status = TaskStatusFactory(
            task_id='test-task-123',
            deal=deal,
            status=TaskStatus.PROCESSING,
            message='Task is being processed'
        )   
        
        assert task_status.task_id == 'test-task-123'
        assert task_status.deal == deal
        assert task_status.status == TaskStatus.PROCESSING
        assert task_status.message == 'Task is being processed'
        assert task_status.created_at is not None
        assert task_status.updated_at is not None

    def test_task_status_choices(self):
        """Test that task status is limited to valid choices"""
        task_status = TaskStatusFactory(status=TaskStatus.PENDING)
        assert task_status.status in [choice[0] for choice in TaskStatus.STATUS_CHOICES]

    def test_task_status_string_representation(self):
        """Test string representation of TaskStatus"""
        task_status = TaskStatusFactory(task_id='test-123', status=TaskStatus.COMPLETED)
        expected = "test-123 - completed"
        assert str(task_status) == expected

    def test_task_status_ordering(self):
        """Test that task statuses are ordered by created_at descending"""
        task1 = TaskStatusFactory()
        task2 = TaskStatusFactory()
        
        task_statuses = TaskStatus.objects.all()
        assert task_statuses[0] == task2
        assert task_statuses[1] == task1

    def test_task_status_with_completion_time(self):
        """Test task status with completion time"""
        from datetime import datetime
        task_status = TaskStatusFactory(
            status=TaskStatus.COMPLETED,
            completed_at=datetime.now()
        )
        
        assert task_status.status == TaskStatus.COMPLETED
        assert task_status.completed_at is not None
