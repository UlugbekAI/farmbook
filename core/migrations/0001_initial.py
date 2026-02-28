from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('group', models.CharField(choices=[('protection', 'Protection'), ('fertilizer', 'Fertilizer')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('field_type', models.CharField(choices=[('greenhouse', 'Greenhouse'), ('open', 'Open')], max_length=20)),
                ('area', models.DecimalField(decimal_places=2, max_digits=8)),
                ('area_unit', models.CharField(choices=[('sotka', 'Sotka'), ('ha', 'Ha')], default='sotka', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='IrrigationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('water_liters', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration_min', models.PositiveIntegerField()),
                ('notes', models.TextField(blank=True)),
                ('crop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='irrigation_logs', to='core.crop')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='irrigation_logs', to='core.field')),
            ],
            options={'ordering': ['-date_time']},
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('kind', models.CharField(choices=[('disease', 'Disease'), ('pest', 'Pest'), ('deficiency', 'Deficiency')], max_length=20)),
                ('short_description', models.CharField(blank=True, max_length=300)),
                ('symptoms', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='issues/')),
                ('crop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='core.crop')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('active_ingredient', models.CharField(blank=True, max_length=200)),
                ('formulation', models.CharField(blank=True, max_length=200)),
                ('notes', models.TextField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='core.category')),
            ],
        ),
        migrations.CreateModel(
            name='SprayLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('water_rate_note', models.CharField(blank=True, max_length=200)),
                ('notes', models.TextField(blank=True)),
                ('crop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spray_logs', to='core.crop')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spray_logs', to='core.field')),
                ('target_issue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='spray_logs', to='core.issue')),
            ],
            options={'ordering': ['-date_time']},
        ),
        migrations.CreateModel(
            name='SprayMixItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dose_text', models.CharField(max_length=120)),
                ('notes', models.TextField(blank=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spray_mix_items', to='core.product')),
                ('spray', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mix_items', to='core.spraylog')),
            ],
        ),
        migrations.CreateModel(
            name='IssueRecommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveIntegerField(default=1)),
                ('note', models.TextField(blank=True)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations', to='core.issue')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_recommendations', to='core.product')),
            ],
            options={'ordering': ['rank', 'id'], 'unique_together': {('issue', 'product')}},
        ),
        migrations.CreateModel(
            name='DosageRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dose_10l_value', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('dose_10l_unit', models.CharField(blank=True, choices=[('ml_10l', 'ml/10L'), ('g_10l', 'g/10L')], max_length=20)),
                ('dose_per_ha_value', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('dose_per_ha_unit', models.CharField(blank=True, choices=[('l_ha', 'L/ha'), ('kg_ha', 'kg/ha')], max_length=20)),
                ('interval_days', models.PositiveIntegerField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('crop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dosage_rules', to='core.crop')),
                ('issue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dosage_rules', to='core.issue')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dosage_rules', to='core.product')),
            ],
        ),
    ]
