# Generated by Django 3.0.7 on 2020-07-25 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigndata', '0003_auto_20200709_1925'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donation',
            options={'ordering': ['donor']},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='address',
            name='name',
        ),
        migrations.AlterField(
            model_name='donation',
            name='donation_amount',
            field=models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Donation amount $'),
        ),
        migrations.AddConstraint(
            model_name='organization',
            constraint=models.UniqueConstraint(fields=('name',), name='unique name'),
        ),
    ]
