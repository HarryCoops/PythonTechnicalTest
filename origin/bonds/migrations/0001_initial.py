# Generated by Django 2.2.13 on 2020-12-19 23:32

import bonds.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isin', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator('[A-Z0-9]*')])),
                ('size', models.IntegerField(validators=[bonds.models.validate_positive])),
                ('currency', models.CharField(max_length=3, validators=[bonds.models.validate_currency_code])),
                ('maturity', models.DateField()),
                ('lei', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('[A-Z0-9]*')])),
                ('legal_name', models.CharField(max_length=100)),
                ('created', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='bond',
            index=models.Index(fields=['user', 'isin'], name='bonds_bond_user_id_03e624_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='bond',
            unique_together={('user', 'isin')},
        ),
    ]
