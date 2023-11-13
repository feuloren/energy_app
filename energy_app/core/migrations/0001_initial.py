# Generated by Django 4.2.7 on 2023-11-12 20:25

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
            name='Appliance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('power', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ApplianceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('minimum_operating_hours', models.PositiveIntegerField()),
                ('maximum_operating_hours', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HomeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_energy_consumption', models.IntegerField()),
                ('appliances', models.ManyToManyField(to='core.appliance')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='appliance',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.appliancecategory'),
        ),
    ]
