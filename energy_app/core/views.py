from django.shortcuts import render
from django.views.generic.edit import FormView

from energy_app.core.forms import HomeProfilePublicForm
from energy_app.core.rules import estimate_runtime_by_appliance


class HomeProfilePublicView(FormView):
    template_name = 'public_home_profile_form.html'
    form_class = HomeProfilePublicForm

    def form_valid(self, form):
        data = form.cleaned_data

        total_energy_consumption = data['total_energy_consumption'] * 1000
        appliances_stats = [
            {
                'name': appliance.name,
                'daily_power': appliance.power * runtime,
                'percent': appliance.power * runtime / total_energy_consumption * 100
            }
            for appliance, runtime in estimate_runtime_by_appliance(data['appliances'], total_energy_consumption).items()
        ]

        return render(self.request, 'public_home_profile_summary.html', context={
            'email': data['email'],
            'total_energy_consumption': data['total_energy_consumption'],
            'appliances_stats': appliances_stats
        })
