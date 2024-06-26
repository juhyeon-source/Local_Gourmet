# Generated by Django 4.2 on 2024-05-26 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StoreAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_si', models.CharField(max_length=10)),
                ('address_gu', models.CharField(max_length=10)),
                ('address_detail', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('Korean', '한식'), ('Chinese', '중식'), ('Japanese', '일식'), ('Western', '양식'), ('Dessert', '디저트'), ('Pub', '주점'), ('FastFood', '패스트푸드'), ('Other', '기타')], max_length=10)),
                ('phone_number', models.CharField(max_length=13)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stores.storeaddress')),
            ],
        ),
    ]
