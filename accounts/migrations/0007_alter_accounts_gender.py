# Generated by Django 4.2 on 2024-05-23 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_accounts_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', '남성'), ('F', '여성'), ('-', '--')], default='-', max_length=1),
        ),
    ]
