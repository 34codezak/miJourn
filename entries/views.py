# entries/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EntryForm, MultiDeleteForm, SearchForm
from .models import Entry

# Entry view
@login_required
def home(request):
    entries = Entry.objects.filter(user=request.user).order_by('-created_at')[:5]
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

            # Using keyword args
            return redirect('entries:view_entry', entry.id)
    else:
        form = EntryForm()
    
    return render(request, 'entries/create_entry.html', {'form': form})

    
    

# Update entry view

@login_required
def update_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
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
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('entries:home')
    return render(request, 'entries/delete_entry.html', {'entry': entry})

# View entry view
@login_required
def view_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)
    return render(request, 'entries/view_entry.html', {'entry': entry})

# View all entries view
@login_required
def view_all_entries(request):
    entries = Entry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'entries/all_entries.html', {'entries': entries})


# View entry details view
def view_entry_details(request):
    return render(request, 'entries/entry_details.html')

@login_required
def search_entries(request):
    form = SearchForm(request.GET or None)
    results = []
    query = ''

    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            results = Entry.objects.filter(user=request.user).filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )

    context = {
        'form': form,
        'results': results,
        'query': query,
    }

    return render(request, 'entries/search_entries.html', context)

@login_required
def multi_delete(request):
    if request.method == 'POST':
        form = MultiDeleteForm(request.POST, user=request.user)
        if form.is_valid():
            selected = form.cleaned_data['selections']
            count = selected.count()
            selected.delete()
            messages.success(request, f'Deleted {count} entries successfully.')
            return redirect('entries:view_all_entries')
    else:
        form = MultiDeleteForm(user=request.user)

    return render(request, 'entries/multi_delete.html', {'form': form})