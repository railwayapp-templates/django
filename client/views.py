from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from django.db.models import Count

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Client
from .forms import ClientForm
from .serializer import ClientSerializer

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


class ClientsViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]