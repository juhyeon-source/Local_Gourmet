
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0011_remove_accounts_address_accounts_address_detail_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StoreAddress",
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
                ("address_si", models.CharField(max_length=10)),
                ("address_gu", models.CharField(max_length=10)),
                ("address_detail", models.CharField(max_length=100)),
            ],
        ),
    ]
