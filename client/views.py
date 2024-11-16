from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from django.db.models import Count
from .models import Client
from .forms import ClientForm

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            # Return template with success message
            return render(request, 'add_client.html', {'form': form, 'success': 'Client added successfully!'})
    else:
        form = ClientForm()
    return render(request, 'add_client.html', {'form': form})

class ClientDashboardView(TemplateView):
    template_name = "client_dashboard.html"
    title = _("Client Dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        total_clients = Client.objects.count()
        clients_by_ethnicity = Client.objects.values('ethnicity').annotate(count=Count('id')).order_by('ethnicity')
        
        # Convert choices list of tuples to a dictionary
        ethnicity_choices = dict(Client._meta.get_field('ethnicity').choices)

        ethnicity_breakdown = [
            {
                "title": ethnicity_choices.get(ethnicity['ethnicity'], 'Unknown'),
                "value": ethnicity['count']
            }
            for ethnicity in clients_by_ethnicity
        ]
                
        context.update(
            {
                "total_clients": total_clients,
                "ethnicity_breakdown": ethnicity_breakdown,
            }
        )
        return context