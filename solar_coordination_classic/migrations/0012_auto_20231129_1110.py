# Generated by Django 4.2.2 on 2023-11-29 11:10

from django.db import migrations

def add_default_comfort_cost_slot(apps, schema_editor):
    ComfortProfile = apps.get_model('solar_coordination_classic', 'ComfortProfile')
    ComfortCostSlot = apps.get_model('solar_coordination_classic', 'ComfortCostSlot')

    default_profile = ComfortProfile.objects.get(name = "9am to 3pm")
    hours = [i for i in range(1, 25)]
    reward_values = [0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.40, 0.30, 0.20, 0.10, 0.20, 0.30, 0.40, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50]

    for hour, reward_value in zip(reversed(hours), reversed(reward_values)):
        ComfortCostSlot(hour = hour, cost = reward_value, comfort_profile = default_profile).save()

def remove_default_comfort_cost_slot(apps, schema_editor):
    ComfortProfile = apps.get_model('solar_coordination_classic', 'ComfortProfile')
    ComfortCostSlot = apps.get_model('solar_coordination_classic', 'ComfortCostSlot')
    
    default_profile = ComfortProfile.objects.get(name = "9am to 3pm")
    ComfortCostSlot.objects.filter(comfort_profile = default_profile).delete()

class Migration(migrations.Migration):

    dependencies = [
        ("solar_coordination_classic", "0011_auto_20231129_1104"),
    ]

    operations = [
        migrations.RunPython(code = add_default_comfort_cost_slot, reverse_code = remove_default_comfort_cost_slot),
    ]
