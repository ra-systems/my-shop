# Generated by Django 4.2.1 on 2023-05-10 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import erp_framework.base.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date and time')),
                ('lastmod', models.DateTimeField(db_index=True, verbose_name='last modification')),
                ('slug', models.SlugField(blank=True, help_text='For fast recall', unique=True, verbose_name='Identifier slug')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Name')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('lastmod_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_lastmod_related', to=settings.AUTH_USER_MODEL, verbose_name='last modification by')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_related', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'abstract': False,
            },
            bases=(erp_framework.base.models.ERPMixin, erp_framework.base.models.DiffingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Product Name')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=100, verbose_name='Sale Number')),
                ('date', models.DateTimeField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('value', models.DecimalField(decimal_places=2, editable=False, max_digits=9)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.client')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.product')),
            ],
        ),
    ]