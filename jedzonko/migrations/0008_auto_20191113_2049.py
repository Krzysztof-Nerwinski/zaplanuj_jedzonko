# Generated by Django 2.2.6 on 2019-11-13 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0007_recipe_instructions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayname',
            name='day_name',
            field=models.CharField(choices=[('MON', 'Poniedziałek'), ('TUE', 'Wtorek'), ('WED', 'Środa'), ('THU', 'Czwartek'), ('FRI', 'Piątek'), ('SAT', 'Sobota'), ('SUN', 'Niedziela')], max_length=3),
        ),
    ]
