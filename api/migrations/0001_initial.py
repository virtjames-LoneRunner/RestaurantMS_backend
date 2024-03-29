# Generated by Django 4.0.2 on 2022-04-09 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('category', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventory_item', models.CharField(max_length=255)),
                ('item_category', models.CharField(max_length=255)),
                ('quantity', models.FloatField()),
                ('reorder_quantity', models.FloatField()),
                ('unit', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.BooleanField(default=True)),
                ('menu_item', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=10)),
                ('unit_price', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.categories')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.menuitems')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cashier_id', models.CharField(max_length=10)),
                ('transaction_id', models.CharField(max_length=50)),
                ('transaction_type', models.CharField(max_length=50)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('table_number', models.IntegerField()),
                ('total_amount', models.FloatField()),
                ('amount_given', models.FloatField()),
                ('discount', models.FloatField()),
                ('change', models.FloatField()),
                ('address', models.CharField(max_length=255)),
                ('items', models.ManyToManyField(through='api.TransactionItems', to='api.MenuItems')),
            ],
        ),
        migrations.AddField(
            model_name='transactionitems',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.transactions'),
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=100)),
                ('unit_price', models.FloatField()),
                ('unit', models.CharField(max_length=10)),
                ('pcs', models.IntegerField()),
                ('transaction_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.transactions')),
            ],
        ),
    ]
