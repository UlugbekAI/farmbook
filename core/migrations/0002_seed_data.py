from django.db import migrations


def seed_data(apps, schema_editor):
    Crop = apps.get_model('core', 'Crop')
    Field = apps.get_model('core', 'Field')
    Category = apps.get_model('core', 'Category')

    Crop.objects.get_or_create(name='Strawberry')
    Field.objects.get_or_create(
        name='Strawberry Greenhouse',
        defaults={'field_type': 'greenhouse', 'area': 22, 'area_unit': 'sotka'},
    )
    Field.objects.get_or_create(
        name='Strawberry Open Field',
        defaults={'field_type': 'open', 'area': 40, 'area_unit': 'sotka'},
    )
    Category.objects.get_or_create(name='Plant Protection', group='protection')
    Category.objects.get_or_create(name='Fertilizers', group='fertilizer')


def reverse_seed(apps, schema_editor):
    Crop = apps.get_model('core', 'Crop')
    Field = apps.get_model('core', 'Field')
    Category = apps.get_model('core', 'Category')

    Crop.objects.filter(name='Strawberry').delete()
    Field.objects.filter(name__in=['Strawberry Greenhouse', 'Strawberry Open Field']).delete()
    Category.objects.filter(name__in=['Plant Protection', 'Fertilizers']).delete()


class Migration(migrations.Migration):

    dependencies = [('core', '0001_initial')]

    operations = [migrations.RunPython(seed_data, reverse_seed)]
