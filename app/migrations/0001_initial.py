"""File with migration details"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Class needed to migration"""

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Transaction",
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
                (
                    "type",
                    models.CharField(
                        choices=[("i", "Income"), ("e", "Expense")], max_length=1
                    ),
                ),
                ("value", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "expense_category",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "job_address",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
            ],
        ),
    ]
