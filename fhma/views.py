import json
import random

from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView, TemplateView
from unfold.views import UnfoldModelAdminViewMixin

from client.models import Client, AreaServiced
from equipment.models import Order
from supplies.models import Supplies, SuppliesOrder

class HomeView(RedirectView):
    pattern_name = "admin:index"


class MyClassBasedView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Home Dashboard"  # required: custom page header title
    permission_required = ()  # required: tuple of permissions
    template_name = "formula/driver_custom_page.html"

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

def dashboard_callback(request, context):
    WEEKDAYS = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]

    total_number_of_clients = Client.objects.count()
    total_number_of_outstanding_rentals = Order.objects.filter(status="RT").count()
    total_number_of_inconcient_supplies = SuppliesOrder.objects.count()

    performance_positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
    performance_negative = [
        [-1, -random.randrange(8, 28)] for i in range(1, 28)]

    context.update(
        {
            "navigation": [
                {"title": _("Dashboard"), "link": "/", "active": True},
                {"title": _("Equipment Dashboard"), "link": "#"},
                {"title": _("Supplies Dashboard"), "link": "#"},
                {"title": _("Client Dashboard"), "link": "#"},
            ],
            "filters": [
                {"title": _("All"), "link": "#", "active": True},
                {
                    "title": _("Last 30 Days"),
                    "link": "#",
                },
            ],
            "kpi": [
                {
                    "title": "Number of Clients Surived",
                    "metric": f"{intcomma(total_number_of_clients)}",
                    "footer": mark_safe(
                        f'Total number of clients reached and logged in the system'
                    ),
                },
                {
                    "title": "Number of Outstanding Rentals",
                    "metric": f"{intcomma(total_number_of_outstanding_rentals)}",
                    "footer": mark_safe(
                        f'Total number of medical equipment rented out and not returned'
                    ),
                },
                {
                    "title": "Total number of inconcient supplies handed out",
                    "metric": f"{intcomma(total_number_of_inconcient_supplies)}",
                    "footer": mark_safe(
                        f'Total number of inconcient supply orders handed out'
                    ),
                },
            ],
            "zipcode_breakdown": update_areaservice_breakdown(),
            "performance": [
                {
                    "title": _("Last week revenue"),
                    "metric": "$1,234.56",
                    "footer": mark_safe(
                        '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                    ),
                    "chart": json.dumps(
                        {
                            "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                            "datasets": [
                                {"data": performance_positive,
                                    "borderColor": "#9333ea"}
                            ],
                        }
                    ),
                },
                {
                    "title": _("Last week expenses"),
                    "metric": "$1,234.56",
                    "footer": mark_safe(
                        '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                    ),
                    "chart": json.dumps(
                        {
                            "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                            "datasets": [
                                {"data": performance_negative,
                                    "borderColor": "#f43f5e"}
                            ],
                        }
                    ),
                },
            ],
        },
    )

    return context
