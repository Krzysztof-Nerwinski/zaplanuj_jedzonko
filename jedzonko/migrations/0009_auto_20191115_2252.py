# Generated by Django 2.2.6 on 2019-11-15 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0008_auto_20191113_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayname',
            name='day_name',
            field=models.CharField(choices=[('PON', 'Poniedziałek'), ('WTO', 'Wtorek'), ('ŚRO', 'Środa'), ('CZW', 'Czwartek'), ('PT', 'Piątek'), ('SB', 'Sobota'), ('NDZ', 'Niedziela')], max_length=3),
        ),
    ]
