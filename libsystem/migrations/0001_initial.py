# Generated by Django 4.1 on 2022-09-07 07:26

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('1', 'Active'), ('3', 'Deleted'), ('2', 'Inactive')], default='2', max_length=1)),
                ('a_id', models.UUIDField(default=uuid.UUID('e35c1821-92a0-4f85-8c64-f34e6b7a4f49'), editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('meta_data', models.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('1', 'Active'), ('3', 'Deleted'), ('2', 'Inactive')], default='2', max_length=1)),
                ('book_id', models.UUIDField(default=uuid.UUID('bc11e53e-287f-46e9-9704-cc3e7c6ba2c4'), editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('extra_details', models.JSONField(blank=True, null=True)),
                ('is_ebook', models.BooleanField(blank=True, choices=[(True, 'Yes, there exist an EBook'), (False, 'No, not an Ebook')], null=True)),
                ('authors', models.ManyToManyField(blank=True, null=True, to='libsystem.author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('1', 'Active'), ('3', 'Deleted'), ('2', 'Inactive')], default='2', max_length=1)),
                ('lang_id', models.UUIDField(default=uuid.UUID('9183370e-a252-42f4-b4b7-83706c1536fa'), editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('script', models.TextField(blank=True, null=True)),
                ('about', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('1', 'Active'), ('3', 'Deleted'), ('2', 'Inactive')], default='2', max_length=1)),
                ('pub_id', models.UUIDField(default=uuid.UUID('d193be6e-c3eb-48f8-b929-5b377ec70bd9'), editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('meta_data', models.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('1', 'Active'), ('3', 'Deleted'), ('2', 'Inactive')], default='2', max_length=1)),
                ('first_name', models.CharField(max_length=200)),
                ('middle_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('email', models.EmailField(max_length=254)),
                ('meta_data', models.JSONField(blank=True, null=True)),
                ('role', models.CharField(choices=[('3', 'User'), ('1', 'Super Admin'), ('2', 'Librarian')], default='3', max_length=1)),
                ('subscription', models.BooleanField(default=False)),
                ('favorites', models.ManyToManyField(blank=True, null=True, to='libsystem.book')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HardCopy',
            fields=[
                ('hardCopy_id', models.UUIDField(default=uuid.UUID('05672c7a-d949-40a4-9c8a-8ac53030859e'), editable=False, primary_key=True, serialize=False)),
                ('isLent', models.BooleanField(default=False)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libsystem.book')),
                ('lentTo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='libsystem.user')),
            ],
        ),
        migrations.CreateModel(
            name='Ebook',
            fields=[
                ('ebook_id', models.UUIDField(default=uuid.UUID('2c35b99f-da6c-4b98-9ae0-bc6488a15b10'), editable=False, primary_key=True, serialize=False)),
                ('book_location', models.CharField(blank=True, max_length=200, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ebook', to='libsystem.book')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='languages',
            field=models.ManyToManyField(blank=True, null=True, to='libsystem.language'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libsystem.publisher'),
        ),
    ]
