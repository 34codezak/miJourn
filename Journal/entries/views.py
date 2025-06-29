# entries/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Entry
from .forms import EntryForm
from django.shortcuts import get_object_or_404
from . import models

# Entry view
def home(request):
    entries = models.Entry.objects.order_by('-created_at')[:5]
    return render(request, 'entries/home.html', {'entries': entries})

# Create entry view
@login_required
def create_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False) 
            entry.user = request.user
            entry.save()
            return render(request, 'entries/view_entry.html', entry_id=entry.id) 
    else:
        form = EntryForm()
    
    return render(request, 'entries/create_entry.html', {'form': form})
    

# Update entry view

@login_required
def update_entry(request, entry_id):
    entry = get_object_or_404(models.Entry, id=entry_id, user=request.user)
    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('entries:view_entry', entry_id=entry.id)
    else:
        form = EntryForm(instance=entry)
    
    return render(request, 'entries/update_entry.html', {'form': form, 'entry': entry})


# Delete entry view
@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(models.Entry, id=entry_id)
    if request.method == 'POST':
        entry.delete()
        return redirect('entries:home')
    return render(request, 'entries/delete_confirm.html', {'entry': entry})

# View entry view
def view_entry(request, entry_id):
    entry = get_object_or_404(models.Entry, id=entry_id)
    return render(request, 'entries/view_entry.html', {'entry': entry})

# View all entries view
def view_all_entries(request):
    entries = models.Entry.objects.all().order_by('-created_at')  # Fixed variable name
    return render(request, 'entries/all_entries.html', {'entries': entries})


# View entry details view
def view_entry_details(request):
    return render(request, 'entries/entry_details.html')
