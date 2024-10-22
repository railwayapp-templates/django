import json
import random
from datetime import datetime, timedelta

from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView, TemplateView
from django.db.models.functions import TruncDay
from django.db.models import F, Count

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
    total_number_of_rentals = Order.objects.count()
    total_number_of_inconcient_supplies = SuppliesOrder.objects.count()

    ## INCONCIENT SUPPLIES OVER TIME
    # Calculate the date 90 days ago
    ninety_days_ago = datetime.now() - timedelta(days=90)

    # Get SuppliesOrder over the last 90 days
    recent_supplies_orders = SuppliesOrder.objects.filter(delivery_date__gte=ninety_days_ago)
    # Annotate and group by date
    orders_by_date = recent_supplies_orders.annotate(date=F('delivery_date')).values('date').annotate(count=Count('id')).order_by('date')
    # Extract dates and counts
    supplies_dates = [order['date'].strftime('%B %d, %Y') for order in orders_by_date]
    supplies_counts = [order['count'] for order in orders_by_date]

    ## EQUIPMENT ORDERS OVER TIME
    # Get Order over the last 90 days
    recent_orders = Order.objects.filter(last_updated__gte=ninety_days_ago)
    # Annotate and group by date
    orders_by_date = recent_orders.annotate(date=F('last_updated')).values('date').annotate(count=Count('id')).order_by('date')
    # Extract dates and counts
    orders_dates = [order['date'].strftime('%B %d, %Y') for order in orders_by_date]
    orders_counts = [order['count'] for order in orders_by_date]

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
                    "title": _("Inconcient Supplies Over Times"),
                    "metric": f"{intcomma(total_number_of_inconcient_supplies)}",
                    "footer": mark_safe(
                        'Inconcient supplies handed out over the last 90 days'
                    ),
                    "chart": json.dumps(
                        {
                            "labels": supplies_dates,
                            "datasets": [
                                {"data": supplies_counts,
                                    "borderColor": "#9333ea"}
                            ],
                        }
                    ),
                },
                {
                    "title": _("Equipment Rentals Over Time"),
                    "metric": f"{intcomma(total_number_of_rentals)}",
                    "footer": mark_safe(
                        'Medical equipment rented out over the last 90 days'
                    ),
                    "chart": json.dumps(
                        {
                            "labels": orders_dates,
                            "datasets": [
                                {"data": orders_counts,
                                    "borderColor": "#f43f5e"}
                            ],
                        }
                    ),
                },
            ],
        },
    )

    return context
