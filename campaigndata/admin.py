from django.contrib import admin
from .models import Donor, PhoneNumber, Address, Marriage, Organization, Donation

admin.site.register(PhoneNumber)
admin.site.register(Address)
admin.site.register(Marriage)

class PhoneInline(admin.TabularInline):
    model = PhoneNumber
    extra = 0


class AddressInlineDonor(admin.StackedInline):
    model = Address
    extra = 1
    exclude = ('organization',)

class AddressInlineOrganization(admin.StackedInline):
    model = Address
    extra = 1
    exclude = ('donor',)


class MarriageInline(admin.TabularInline):
    model = Marriage
    fk_name = 'spouse2'
    extra=0

@admin.register(Organization)
class OrganizationInline(admin.ModelAdmin):
    inlines = [AddressInlineOrganization]

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',  'email',)
    inlines = [AddressInlineDonor, PhoneInline, MarriageInline]
    exclude = ('address',)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'donation_amount', 'donation_date')
