from django.shortcuts import render, redirect
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