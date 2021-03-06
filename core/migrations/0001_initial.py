# Generated by Django 2.2 on 2020-06-02 06:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=150)),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=200)),
                ('bank', models.CharField(max_length=50)),
                ('branch_name', models.CharField(max_length=50)),
                ('amount', models.IntegerField()),
                ('atm_card_number', models.CharField(max_length=8, unique=True)),
                ('atm_card_pin', models.CharField(max_length=4)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
