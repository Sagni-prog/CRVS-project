# Generated by Django 4.0.6 on 2023-02-03 18:42

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[(1, 'Systemadmin'), (2, 'Resident'), (3, 'KebeleEmployee')], default=1, max_length=10)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('username', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('is_resident', models.BooleanField(default=False)),
                ('is_systemadmin', models.BooleanField(default=False)),
                ('is_KebeleEmployee', models.BooleanField(default=False)),
                ('avatar', models.ImageField(default='avatar.svg', null=True, upload_to='')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Kebele',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('kebele_name', models.CharField(help_text='Required', max_length=255, unique=True)),
                ('phone', models.CharField(help_text='Required', max_length=20, null=True)),
                ('email', models.EmailField(help_text='Required', max_length=254, null=True)),
                ('address', models.CharField(help_text='Required', max_length=150, null=True, verbose_name='City')),
                ('po_number', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Kebele',
                'verbose_name_plural': 'Kebeles',
            },
        ),
        migrations.CreateModel(
            name='KebeleEmployee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('address', models.TextField()),
                ('is_employee', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'KebeleEmployee',
                'verbose_name_plural': 'KebeleEmployees',
            },
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=50, null=True)),
                ('age', models.IntegerField(default=0)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('address', models.CharField(max_length=150, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Faleme', 'Famele'), ('No', 'No')], max_length=50)),
                ('current_status', models.CharField(choices=[('singel', 'singel'), ('married', 'married')], max_length=50)),
                ('marital_status', models.IntegerField(default=0)),
                ('avatar', models.ImageField(default='avatar.svg', null=True, upload_to='')),
                ('is_resident', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('kebele', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='entry.kebele')),
            ],
            options={
                'verbose_name': 'Resident',
                'verbose_name_plural': 'Residents',
            },
        ),
        migrations.CreateModel(
            name='VitalEvant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_resident', models.BooleanField(default=False)),
                ('brith_date', models.DateTimeField(auto_now=True)),
                ('death_date', models.DateTimeField(auto_now=True)),
                ('record_date', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Kebele', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='kebeless', to='entry.kebele')),
                ('resident', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reisdent', to='entry.resident')),
            ],
        ),
        migrations.CreateModel(
            name='SystemAdmin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification_Kebele_employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kebeleEmploye_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entry.kebeleemployee')),
            ],
        ),
        migrations.CreateModel(
            name='Marriage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('marital_status', models.CharField(choices=[('singel', 'singel'), ('married', 'married')], default=False, max_length=100)),
                ('brith_date', models.DateTimeField(auto_now=True)),
                ('marriage_date', models.DateTimeField(auto_now=True)),
                ('is_resident', models.BooleanField(default=False)),
                ('record_date', models.DateTimeField(auto_now=True)),
                ('given_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='entry.kebeleemployee')),
                ('kebele', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='kebeles', to='entry.kebele')),
                ('residenr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='residents', to='entry.resident')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveReportKebele_employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_date', models.CharField(max_length=255)),
                ('leave_message', models.TextField()),
                ('leave_status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kebele_employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entry.kebeleemployee')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBackSkebele_employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField()),
                ('feedback_reply', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('KebeleEmploye_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entry.kebeleemployee')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBackResident',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField()),
                ('feedback_reply', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('resident_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entry.resident')),
            ],
        ),
        migrations.CreateModel(
            name='Death',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('marital_status', models.CharField(choices=[('singel', 'singel'), ('married', 'married')], max_length=10)),
                ('death_date', models.DateTimeField(auto_now=True)),
                ('is_resident', models.BooleanField(default=False)),
                ('record_date', models.DateTimeField(auto_now=True)),
                ('given_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='entry.kebeleemployee')),
                ('kebele', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='kebelesa', to='entry.kebele')),
                ('residenr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='resident', to='entry.resident')),
            ],
        ),
        migrations.CreateModel(
            name='Brith',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('marital_status', models.CharField(choices=[('singel', 'singel'), ('married', 'married')], default=False, max_length=100)),
                ('brith_date', models.DateTimeField(auto_now=True)),
                ('is_resident', models.BooleanField(default=False)),
                ('record_date', models.DateTimeField(auto_now=True)),
                ('given_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='entry.kebeleemployee')),
                ('kebele', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kebelessss', to='entry.kebele')),
                ('residenr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='residentssa', to='entry.resident')),
            ],
        ),
    ]
