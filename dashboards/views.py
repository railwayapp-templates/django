from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.translation import gettext_lazy as _

from django.db.models import Count

from unfold.views import UnfoldModelAdminViewMixin

from client.models import Client, AreaServiced


def update_areaservice_breakdown():
    # Fetch all areas serviced
    areas_serviced = AreaServiced.objects.all()

    # Create the updated zipcode breakdown list
    breakdown = []
    for area in areas_serviced:
        count = Client.objects.filter(area_serviced=area).count()
        breakdown.append({
            "title": area.name + ' (' + intcomma(count) + ')',
            "description": area.zipcode,
            "value": count
        })

    return breakdown

# Cusom client dashboard view


class ClientDashboardView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Client Dashboard"  # required: custom page header title
    permission_required = ()  # required: tuple of permissions
    template_name = "client_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_clients = Client.objects.count()
        clients_by_ethnicity = Client.objects.values(
            'ethnicity').annotate(count=Count('id')).order_by('ethnicity')

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
                "navigation": [
                    {"title": _("Dashboard"), "link": "/", "active": True},
                    {"title": _("Equipment Dashboard"), "link": "#"},
                    {"title": _("Supplies Dashboard"), "link": "#"},
                    {"title": _( "Client Dashboard"), "link": "/dashboards/clientdashboard/dashboards/client"},
                ],
                "total_clients": total_clients,
                "ethnicity_breakdown": ethnicity_breakdown,
                "zipcode_breakdown": update_areaservice_breakdown()
            }
        )
        return context
