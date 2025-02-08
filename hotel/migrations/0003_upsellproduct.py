# Generated by Django 4.2.2 on 2025-02-08 21:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_hotel_pms'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpsellProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upsell_id', models.UUIDField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('pms_id', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(choices=[('BREAKFAST', 'Breakfast'), ('PARKING', 'Parking'), ('OTHER', 'Other')], max_length=50)),
                ('is_bookable', models.BooleanField(default=True)),
                ('min_age', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('max_age', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=3)),
                ('per_whom', models.CharField(choices=[('ROOM', 'Per Room'), ('GUEST', 'Per Guest')], max_length=10)),
                ('max_cap_per_stay', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('availability_when', models.CharField(choices=[('ENTIRE_STAY', 'Entire Stay'), ('ON_ARRIVAL', 'Only on Arrival'), ('ON_DEPARTURE', 'Only on Departure')], max_length=20)),
                ('offered_days', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upsell_products', to='hotel.hotel')),
            ],
        ),
    ]
