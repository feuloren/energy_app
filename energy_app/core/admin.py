from django.contrib import admin

from energy_app.core.models import ApplianceCategory, Appliance, HomeProfile
from energy_app.core.rules import estimate_runtime_by_appliance
from energy_app.core.forms import HomeProfileAdminForm


@admin.register(ApplianceCategory)
class ApplianceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'minimum_operating_hours', 'maximum_operating_hours']


@admin.register(Appliance)
class ApplianceAdimn(admin.ModelAdmin):
    list_display = ['name', 'category', 'power']
    list_select_related = ['category']


@admin.register(HomeProfile)
class HomeProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'appliances', 'total_energy_consumption', 'summary']
    
    readonly_fields = ['summary']
    form = HomeProfileAdminForm

    def summary(self, home_profile):
        if not home_profile.total_energy_consumption:
            return ''

        total_power = home_profile.total_energy_consumption_in_watts_hours
        runtime_by_appliance = estimate_runtime_by_appliance(home_profile.appliances.all(), total_power)
        print(runtime_by_appliance)
        return '\n'.join(
            f'{appliance.name}: {runtime * appliance.power / 1000}kWh ({(runtime * appliance.power) / total_power * 100}%)'
            for appliance, runtime in runtime_by_appliance.items()
        )
