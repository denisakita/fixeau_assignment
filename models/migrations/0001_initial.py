# Generated by Django 4.2.6 on 2023-10-14 11:47

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="GroundWater",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("measurement", models.FloatField()),
            ],
            options={
                "verbose_name": "GroundWater",
                "verbose_name_plural": "GroundWaters",
                "db_table": "drf_groundwater",
                "ordering": ["date", "measurement"],
            },
        ),
    ]
