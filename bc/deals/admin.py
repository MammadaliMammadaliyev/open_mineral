from django.contrib import admin
from .models import (DropdownOption, NewBusinessConfirmation, CommercialTerms, 
                     AdditionalClause, PaymentTerms, BusinessConfirmationDeal)


admin.site.register(DropdownOption)
admin.site.register(NewBusinessConfirmation)
admin.site.register(CommercialTerms)
admin.site.register(AdditionalClause)
admin.site.register(PaymentTerms)
admin.site.register(BusinessConfirmationDeal)