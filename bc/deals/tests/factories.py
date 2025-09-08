import factory
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, datetime
from deals.models import (
    NewBusinessConfirmation, BusinessConfirmationDeal, 
    CommercialTerms, PaymentTerms, DropdownOption,
    AdditionalClause, TaskStatus
)

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True


class NewBusinessConfirmationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NewBusinessConfirmation

    seller = factory.Faker('company')
    buyer = factory.Faker('company')
    material = factory.Iterator(['Akzhal', 'Lead concentrate', 'Copper ore', 'Zinc concentrate'])
    quantity = factory.LazyFunction(lambda: Decimal('1000.50'))


class CommercialTermsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommercialTerms

    delivery_term = factory.Iterator(['DAP', 'FOB', 'CIF', 'EXW'])
    delivery_point = factory.Faker('city')
    packaging = factory.Iterator(['Big Bags', 'Bulk', 'Drums'])
    transport_mode = factory.Iterator(['Rail', 'Ship', 'Truck'])
    inland_freight_buyer = factory.Faker('boolean')
    shipment_start_date = factory.LazyFunction(lambda: date.today())
    shipment_end_date = factory.LazyFunction(lambda: date.today().replace(day=date.today().day + 30))
    shipment_evenly_distributed = factory.Faker('boolean')
    treatment_charge = factory.LazyFunction(lambda: Decimal('50.00'))
    treatment_charge_unit = 'dmt'
    refining_charge = factory.LazyFunction(lambda: Decimal('25.00'))
    refining_charge_unit = 'dmt'


class PaymentTermsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentTerms

    payment_stage_1_percentage = factory.LazyFunction(lambda: Decimal('30.00'))
    payment_stage_1_days = 30
    payment_stage_2_percentage = factory.LazyFunction(lambda: Decimal('40.00'))
    payment_stage_2_days = 60
    payment_stage_3_percentage = factory.LazyFunction(lambda: Decimal('30.00'))
    payment_stage_3_days = 90
    currency = factory.Iterator(['USD', 'EUR', 'GBP'])
    payment_method = factory.Iterator(['Bank Transfer', 'Letter of Credit', 'Cash'])
    credit_terms_days = 30
    guarantee_required = factory.Faker('boolean')


class DropdownOptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DropdownOption

    field_name = factory.Iterator(['material', 'delivery_term', 'packaging', 'transport_mode'])
    option_values = factory.LazyFunction(lambda: {
        'value': 'test_value',
        'label': 'Test Label'
    })
    display_order = factory.Sequence(lambda n: n)
    tooltip_text = factory.Faker('sentence')
    is_active = True


class AdditionalClauseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdditionalClause

    clause = factory.Faker('sentence')
    clause_type = factory.Iterator(['standard', 'custom', 'regulatory'])
    is_active = True


class BusinessConfirmationDealFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BusinessConfirmationDeal

    user = factory.SubFactory(UserFactory)
    new_business_confirmation = factory.SubFactory(NewBusinessConfirmationFactory)
    commercial_terms = factory.SubFactory(CommercialTermsFactory)
    payment_terms = factory.SubFactory(PaymentTermsFactory)
    status = factory.Iterator(['draft', 'submitted', 'processing', 'completed'])


class TaskStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskStatus

    task_id = factory.Faker('uuid4')
    deal = factory.SubFactory(BusinessConfirmationDealFactory)
    status = factory.Iterator(['pending', 'processing', 'completed', 'failed'])
    message = factory.Faker('sentence')
