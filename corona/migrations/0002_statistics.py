# Generated by Django 3.0.7 on 2020-06-26 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corona', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('symbol', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('mean_2015', models.FloatField(blank=True, default=None, null=True)),
                ('std_2015', models.FloatField(blank=True, default=None, null=True)),
                ('mean_2016', models.FloatField(blank=True, default=None, null=True)),
                ('std_2016', models.FloatField(blank=True, default=None, null=True)),
                ('mean_2017', models.FloatField(blank=True, default=None, null=True)),
                ('std_2017', models.FloatField(blank=True, default=None, null=True)),
                ('mean_2018', models.FloatField(blank=True, default=None, null=True)),
                ('mean_2019', models.FloatField(blank=True, default=None, null=True)),
                ('std_2019', models.FloatField(blank=True, default=None, null=True)),
                ('mean_2020', models.FloatField(blank=True, default=None, null=True)),
                ('std_2020', models.FloatField(blank=True, default=None, null=True)),
            ],
            options={
                'db_table': 'Statistics',
            },
        ),
    ]
