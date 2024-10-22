import json
import random

from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView, TemplateView
from unfold.views import UnfoldModelAdminViewMixin


class HomeView(RedirectView):
    pattern_name = "admin:index"


class MyClassBasedView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Custom Title"  # required: custom page header title
    permission_required = ()  # required: tuple of permissions
    template_name = "formula/driver_custom_page.html"


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

    positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
    negative = [[-1, -random.randrange(8, 28)] for i in range(1, 28)]
    average = [r[1] - random.randint(3, 5) for r in positive]
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
                    "metric": f"200",
                    "footer": mark_safe(
                        f'Total number of clients reached and logged in the system'
                    ),
                },
                {
                    "title": "Number of Outstanding Rentals",
                    "metric": f"12",
                    "footer": mark_safe(
                        f'Total number of medical equipment rented out and not returned'
                    ),
                },
                {
                    "title": "Total number of inconcient supplies handed out",
                    "metric": f"1,234",
                    "footer": mark_safe(
                        f'Total number of inconcient supply orders handed out'
                    ),
                },
            ],
            "zipcode_breakdown": [
                {
                    "title": "85648",
                    "description": "Rio Rico, Tumacacori-Carmen, & Rio Rico",
                    "value": 10,
                },
                {
                    "title": "85616",
                    "description": "Huachuca City, & Whetstone",
                    "value": 27,
                },
                {
                    "title": "85624",
                    "description": "Patagonia, Lochiel, & Harshaw",
                    "value": 8,
                },
                {
                    "title": "85621",
                    "description": "Nogales, Kino Springs, Ruby, & Beyerville",
                    "value": 40,
                },
                {
                    "title": "85637",
                    "description": "Sonoita, & Greaterville",
                    "value": 1,
                },
                {
                    "title": "85603",
                    "description": "Bisbee & Naco",
                    "value": 5,
                },
                {
                    "title": "85607",
                    "description": "Douglas",
                    "value": 32,
                },
                {
                    "title": "85635",
                    "description": "Sierra Vista",
                    "value": 14,
                },
                {
                    "title": "85602",
                    "description": "Benson",
                    "value": 9,
                },
            ],
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
