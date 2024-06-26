# Generated by Django 4.2 on 2024-05-23 08:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accounts",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("M", "남성"), ("F", "여성"), ("P", "비공개")],
                default="P",
                max_length=1,
            ),
        ),
        migrations.AlterField(
            model_name="accounts",
            name="phone_number",
            field=models.CharField(
                blank=True,
                max_length=13,
                validators=[
                    django.core.validators.RegexValidator("010-?\\d{4}-?\\d{4}$")
                ],
            ),
        ),
    ]