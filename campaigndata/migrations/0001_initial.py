# Generated by Django 3.0.7 on 2020-07-10 00:22

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(max_length=100)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_code', models.IntegerField(help_text='Enter a 3 digit area code.', validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(999)])),
                ('prefix', models.IntegerField(help_text='Enter a 3 phone prefix.', validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(999)])),
                ('subscriber_code', models.IntegerField(help_text='Enter a 4 digit subscriber code.', validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(9999)])),
                ('phone_type', models.CharField(choices=[('home', 'Home Phone'), ('home2', 'Home Phone 2'), ('mobile', 'Mobile Phone'), ('work', 'Work Phone')], default=('home', 'Home Phone'), max_length=20)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigndata.Donor')),
            ],
        ),
        migrations.CreateModel(
            name='Marriage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_marriage', models.BooleanField(default=True)),
                ('spouse1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spouse1', to='campaigndata.Donor')),
                ('spouse2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spouse2', to='campaigndata.Donor')),
            ],
        ),
        migrations.AddField(
            model_name='donor',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='campaigndata.Organization'),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='Full name')),
                ('address1', models.CharField(max_length=1024, verbose_name='Address line 1')),
                ('address2', models.CharField(max_length=1024, verbose_name='Address line 2')),
                ('zip_code', models.CharField(max_length=12, verbose_name='ZIP / Postal code')),
                ('city', models.CharField(max_length=1024, verbose_name='City')),
                ('state', models.CharField(max_length=2, verbose_name='State')),
                ('country', models.CharField(blank=True, max_length=3, verbose_name='Country')),
                ('donor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='campaigndata.Donor')),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='campaigndata.Organization')),
            ],
        ),
    ]
