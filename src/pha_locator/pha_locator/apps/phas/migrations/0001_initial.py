# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(choices=[(b'AK', b'Alaska'), (b'AL', b'Alabama'), (b'AR', b'Arkansas'), (b'AS', b'American Samoa'), (b'AZ', b'Arizona'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DC', b'District Of Columbia'), (b'DE', b'Delaware'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'GU', b'Guam'), (b'HI', b'Hawaii'), (b'IA', b'Iowa'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'MA', b'Massachusetts'), (b'MD', b'Maryland'), (b'ME', b'Maine'), (b'MH', b'Marshall Islands'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MO', b'Missouri'), (b'MP', b'Northern Mariana Islands'), (b'MS', b'Mississippi'), (b'MT', b'Montana'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'NE', b'Nebraska'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NV', b'Nevada'), (b'NY', b'New York'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PR', b'Puerto Rico'), (b'PW', b'Palau'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VA', b'Virginia'), (b'VI', b'US Virgin Islands'), (b'VT', b'Vermont'), (b'WA', b'Washington'), (b'WI', b'Wisconsin'), (b'WV', b'West Virginia'), (b'WY', b'Wyoming')], max_length=2)),
                ('zip', models.CharField(max_length=10)),
                ('cityStateZip', models.CharField(blank=True, editable=False, max_length=42)),
            ],
            options={
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('county', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Counties',
            },
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locality', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Localities',
            },
        ),
        migrations.CreateModel(
            name='Pha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=50)),
                ('state', models.CharField(choices=[(b'AK', b'Alaska'), (b'AL', b'Alabama'), (b'AR', b'Arkansas'), (b'AS', b'American Samoa'), (b'AZ', b'Arizona'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DC', b'District Of Columbia'), (b'DE', b'Delaware'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'GU', b'Guam'), (b'HI', b'Hawaii'), (b'IA', b'Iowa'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'MA', b'Massachusetts'), (b'MD', b'Maryland'), (b'ME', b'Maine'), (b'MH', b'Marshall Islands'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MO', b'Missouri'), (b'MP', b'Northern Mariana Islands'), (b'MS', b'Mississippi'), (b'MT', b'Montana'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'NE', b'Nebraska'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NV', b'Nevada'), (b'NY', b'New York'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PR', b'Puerto Rico'), (b'PW', b'Palau'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VA', b'Virginia'), (b'VI', b'US Virgin Islands'), (b'VT', b'Vermont'), (b'WA', b'Washington'), (b'WI', b'Wisconsin'), (b'WV', b'West Virginia'), (b'WY', b'Wyoming')], max_length=2)),
                ('city', models.CharField(max_length=30)),
                ('program', models.CharField(choices=[(b'L', b'Low-Rent'), (b'S8', b'Section 8'), (b'L;S8', b'Combined')], max_length=2)),
                ('low_rent_units', models.IntegerField(default=0)),
                ('section8_units', models.IntegerField(default=0)),
                ('total_units', models.IntegerField(blank=True, editable=False)),
                ('line1', models.CharField(max_length=30)),
                ('line2', models.CharField(blank=True, max_length=30)),
                ('county', models.CharField(max_length=30)),
                ('zip_code', models.CharField(max_length=11)),
                ('phone_number', models.CharField(blank=True, max_length=17)),
                ('fax_number', models.CharField(blank=True, max_length=17)),
                ('TTY_Number', models.CharField(blank=True, max_length=17)),
                ('web_page_address', models.URLField(blank=True)),
                ('email_address', models.EmailField(blank=True, max_length=70)),
                ('mayor', models.CharField(blank=True, max_length=30)),
                ('board_chairperson', models.CharField(blank=True, max_length=30)),
                ('executive_director', models.CharField(blank=True, max_length=30)),
                ('HUD_field_office', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='VPS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Effective', models.DateField()),
                ('PercentOfFMR', models.BooleanField()),
                ('FMRRange', models.SmallIntegerField()),
                ('FMRPercent', models.SmallIntegerField()),
                ('VPS0', models.IntegerField(default=0)),
                ('VPS1', models.IntegerField(default=0)),
                ('VPS2', models.IntegerField(default=0)),
                ('VPS3', models.IntegerField(default=0)),
                ('VPS4', models.IntegerField(default=0)),
                ('VPS5', models.IntegerField(default=0)),
                ('VPS6', models.IntegerField(default=0)),
                ('VPS7', models.IntegerField(default=0)),
                ('VPS8', models.IntegerField(default=0)),
                ('VPS9', models.IntegerField(default=0)),
                ('VPS10', models.IntegerField(default=0)),
                ('VPS11', models.IntegerField(default=0)),
                ('VPSSRO', models.IntegerField(default=0)),
                ('VPSMfg', models.IntegerField(default=0)),
                ('EditBy', models.CharField(max_length=30)),
                ('EditDate', models.DateField()),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phas.County')),
                ('locality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phas.Locality')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phas.County'),
        ),
        migrations.AddField(
            model_name='city',
            name='defaultLocality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phas.Locality'),
        ),
    ]
