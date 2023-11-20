from django.contrib import admin

from .models import EnergyPricing, Condition, SolarGenerationProfile,\
      SolarGeneration, StudyRun, ComfortProfile, ComfortCostSlot,\
          Booking, Participant

# Register your models here.

class EnergyPricingAdmin(admin.ModelAdmin):
    list_display = ("name", "export_price", "import_price", "active",)

admin.site.register(EnergyPricing, EnergyPricingAdmin)


class ConditionAdmin(admin.ModelAdmin):
    list_display = ("ui_type", "group_size",)

admin.site.register(Condition, ConditionAdmin)


class SolarGenerationProfileAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(SolarGenerationProfile, SolarGenerationProfileAdmin)


class SolarGenerationAdmin(admin.ModelAdmin):
    list_display = ("hour", "amount", "solar_generation_profile")

admin.site.register(SolarGeneration, SolarGenerationAdmin)


class StudyRunAdmin(admin.ModelAdmin):
    list_display = ("completed", "solar_generation_profile", "condition")

admin.site.register(StudyRun, StudyRunAdmin)


# class UserAdmin(admin.ModelAdmin):
#     list_display = ("name", "study_run",)

# admin.site.register(User)


class ComfortProfileAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(ComfortProfile, ComfortProfileAdmin)


class ComfortCostSlotAdmin(admin.ModelAdmin):
    list_display = ("hour", "cost", "comfort_profile",)

admin.site.register(ComfortCostSlot, ComfortCostSlotAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "hour", "amount", "created_at", "modified_at", "user",)

admin.site.register(Booking, BookingAdmin)


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("user", "comfort_profile",)

admin.site.register(Participant, ParticipantAdmin)