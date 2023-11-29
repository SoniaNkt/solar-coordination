from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class EnergyPricing(models.Model):
    name = models.CharField(max_length=50, blank=True)
    import_price = models.DecimalField(max_digits=50,decimal_places=2)
    export_price = models.DecimalField(max_digits=50, decimal_places=2)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Condition(models.Model):
    # name = models.CharField(max_length=50)
    ui_type = models.CharField(max_length=50)
    group_size = models.IntegerField()

    active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('ui_type', 'group_size')

    def __str__(self):
        return f"{self.ui_type} ({self.ui_type})"

    def n_participants(self):
        n_participants = Participant.objects.filter(
            condition=self
        ).exclude(
            user__username__startswith='TEST_USER__').count()
        return n_participants

    def n_test_participants(self):
        n_participants = Participant.objects.filter(
            condition=self
        ).filter(
            user__username__startswith='TEST_USER__').count()
        return n_participants



class SolarGenerationProfile(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SolarGeneration(models.Model):
    hour = models.IntegerField()
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    solar_generation_profile = models.ForeignKey(SolarGenerationProfile, on_delete=models.CASCADE, null=True)
    #relationship with 'solar_generation_profile'

class StudyRun(models.Model):
    completed = models.BooleanField(default=False)
    solar_generation_profile = models.ForeignKey(SolarGenerationProfile, on_delete=models.CASCADE, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, null=True)
    #relationship with 'condition' and 'solar_generation_profile'

# class User(models.Model):
#     name = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     study_run = models.ForeignKey(StudyRun, on_delete=models.CASCADE, null=True)
#     #relationship with 'study_run'

#     def __str__(self):
#         return self.name

class ComfortProfile(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ComfortCostSlot(models.Model):
    hour = models.IntegerField()
    cost = models.DecimalField(max_digits=50, decimal_places=2)
    comfort_profile = models.ForeignKey(ComfortProfile, on_delete=models.CASCADE, null=True)
    #relationship with 'comfort_profile'

class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comfort_profile = models.ForeignKey(ComfortProfile, on_delete=models.CASCADE, null=True)
    #relationship with 'user' and 'cost_comfort_profile'
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, null=True)

class Booking(models.Model):
    name = models.CharField(max_length=50)
    hour = models.IntegerField()
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    #relationship with 'user'

    def __str__(self):
        return self.name

class StudyRunAllocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    study_run = models.ForeignKey(StudyRun, on_delete=models.CASCADE, null=True)
