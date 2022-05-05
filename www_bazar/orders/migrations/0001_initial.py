# Generated by Django 4.0.3 on 2022-03-28 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('delivery', models.CharField(choices=[('S', 'Самовывоз'), ('K', 'Доставка курьером '), ('P', 'Доставка почтовой службой ')], default='S', max_length=1)),
                ('payment', models.CharField(choices=[('N', 'Наличные при получении'), ('C', 'Картой'), ('E', 'Электронные деньги'), ('B', 'Банковский перевод')], default='C', max_length=1)),
                ('city', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('oplata', models.BooleanField(default=False)),
                ('bazar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bazar', to='main.bazar')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='main.product')),
            ],
        ),
    ]
