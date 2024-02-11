# Generated by Django 4.0 on 2024-02-11 13:23

from django.db import migrations, models
import django.db.models.deletion
import myapps.core.manager
import myapps.core.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='member.customuser')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, myapps.core.manager.DeleteMixin),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to=myapps.core.models.get_image_path)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='member.customuser')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, myapps.core.manager.DeleteMixin),
        ),
        migrations.CreateModel(
            name='Edites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('field_changed', models.CharField(max_length=100)),
                ('old_value', models.CharField(max_length=100)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s', to='member.customuser')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, myapps.core.manager.DeleteMixin),
        ),
    ]
