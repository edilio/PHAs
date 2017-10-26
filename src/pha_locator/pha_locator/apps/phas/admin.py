
#  Created on Aug 21, 2011
#  @author: edilio


from django.contrib import admin

from . import models


@admin.register(models.Locality)
class LocalityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.County)
class CountyAdmin(admin.ModelAdmin):
    pass


class VPSAdmin(admin.ModelAdmin):
    list_display = ('Effective', 'county', 'VPS0', 'VPS1', 'VPS2', 'VPS3', 'VPS4', 'VPS5', 'VPS6', 'VPS7')


class CityAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', 'zip')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('lastName', 'firstName', 'middleName')


class PHAAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'state', 'program', 'low_rent_units', 'section8_units', 'total_units',
                    'email_address')
    list_filter = ['program', 'state']
    list_per_page = 20
    search_fields = ['code', 'name', 'city']
    ordering = ['name']
    fieldsets = (
        ('General Info', {
            'fields': (('code', 'name'), 'program', ('low_rent_units', 'section8_units', ))
        }),
        ('Address', {
            'classes': ('wide',),
            'fields': (
                    ('line1', 'line2'),
                    ('city', 'county', 'state', 'zip_code'),
            )
        }),
        ('Contact Info', {
            'classes': ('wide',),
            'fields': (
                    ('phone_number', 'fax_number', 'TTY_Number'),
                    ('web_page_address', 'email_address')
            )
        }),
        ('Other Info', {
            'classes': ('collapse',),
            'fields': (
                        ('mayor', 'board_chairperson', 'executive_director', 'HUD_field_office')
            )
        }),
    )


admin.site.register(models.VPS, VPSAdmin)
admin.site.register(models.City, CityAdmin)
admin.site.register(models.Pha, PHAAdmin)
