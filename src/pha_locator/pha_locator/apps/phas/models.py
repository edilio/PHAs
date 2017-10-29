from django.db import models
from django.db.models.signals import pre_save
from .signals import pre_save_pha, pre_save_city


class County(models.Model):
    county = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Counties'

    def __str__(self):
        return self.county


class Locality(models.Model):
    locality = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Localities'

    def __str__(self):
        return self.locality


class VPS(models.Model):

    county = models.ForeignKey(County)
    locality = models.ForeignKey(Locality)

    Effective = models.DateField()
    PercentOfFMR = models.BooleanField()
    FMRRange = models.SmallIntegerField()
    FMRPercent = models.SmallIntegerField()
    VPS0 = models.IntegerField(default=0)
    VPS1 = models.IntegerField(default=0)
    VPS2 = models.IntegerField(default=0)
    VPS3 = models.IntegerField(default=0)
    VPS4 = models.IntegerField(default=0)
    VPS5 = models.IntegerField(default=0)
    VPS6 = models.IntegerField(default=0)
    VPS7 = models.IntegerField(default=0)
    VPS8 = models.IntegerField(default=0)
    VPS9 = models.IntegerField(default=0)
    VPS10 = models.IntegerField(default=0)
    VPS11 = models.IntegerField(default=0)
    VPSSRO = models.IntegerField(default=0)
    VPSMfg = models.IntegerField(default=0)
    EditBy = models.CharField(max_length=30)
    EditDate = models.DateField()


STATE_CHOICES = (
    ('AK', 'Alaska'),
    ('AL', 'Alabama'),
    ('AR', 'Arkansas'),
    ('AS', 'American Samoa'),
    ('AZ', 'Arizona'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DC', 'District Of Columbia'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('GU', 'Guam'),
    ('HI', 'Hawaii'),
    ('IA', 'Iowa'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('MA', 'Massachusetts'),
    ('MD', 'Maryland'),
    ('ME', 'Maine'),
    ('MH', 'Marshall Islands'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MO', 'Missouri'),
    ('MP', 'Northern Mariana Islands'),
    ('MS', 'Mississippi'),
    ('MT', 'Montana'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('NE', 'Nebraska'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NV', 'Nevada'),
    ('NY', 'New York'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('PR', 'Puerto Rico'),
    ('PW', 'Palau'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VA', 'Virginia'),
    ('VI', 'US Virgin Islands'),
    ('VT', 'Vermont'),
    ('WA', 'Washington'),
    ('WI', 'Wisconsin'),
    ('WV', 'West Virginia'),
    ('WY', 'Wyoming'),
    )


class City(models.Model):
    county = models.ForeignKey(County)
    defaultLocality = models.ForeignKey(Locality)
    city = models.CharField(max_length=30)

    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    zip = models.CharField(max_length=10)
    cityStateZip = models.CharField(max_length=42, editable=False, blank=True)

    class Meta:
        verbose_name_plural = 'Cities'



PROGRAM_CHOICES = (
    # ('C', 'Combined'),
    ('L', 'Low-Rent'),
    ('S8', 'Section 8'),
    ('L;S8', 'Combined'),
)

PROGRAM_CHOICES_WITH_ALL = [('All', 'All')] + [(x, y) for x, y in PROGRAM_CHOICES]


class Pha(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    city = models.CharField(max_length=30)
    program = models.CharField(max_length=2, choices=PROGRAM_CHOICES)
    low_rent_units = models.IntegerField(default=0)
    section8_units = models.IntegerField(default=0)
    total_units = models.IntegerField(editable=False, blank=True)
    line1 = models.CharField(max_length=30)
    line2 = models.CharField(max_length=30, blank=True)
    county = models.CharField(max_length=30, blank=True)
    zip_code = models.CharField(max_length=11)

    phone_number = models.CharField(max_length=25, blank=True)
    fax_number = models.CharField(max_length=25, blank=True)
    TTY_Number = models.CharField(max_length=17, blank=True)
    web_page_address = models.URLField(blank=True, max_length=200)
    email_address = models.EmailField(blank=True, max_length=70)
    mayor = models.CharField(max_length=30, blank=True)
    board_chairperson = models.CharField(max_length=30, blank=True)
    executive_director = models.CharField(max_length=30, blank=True)
    HUD_field_office = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


pre_save.connect(pre_save_pha, sender=Pha)
pre_save.connect(pre_save_city, sender=City)
