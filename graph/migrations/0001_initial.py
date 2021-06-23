# Generated by Django 3.2.4 on 2021-06-22 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('nodeId', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('party', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='out_edge', to='graph.node')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_edge', to='graph.node')),
            ],
        ),
    ]
