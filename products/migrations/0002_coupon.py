# Generated by Django 4.1.3 on 2022-11-30 12:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('coupon_code', models.CharField(max_length=100)),
                ('discount', models.IntegerField()),
                ('is_expired', models.BooleanField(default=False)),
                ('minimum_amount', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
