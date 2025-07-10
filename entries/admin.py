from django.contrib import admin
from .models import Entry

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    action = ['delete_selected']

    # Optional: Add a custom action to delete selected entries
    def delete_selected(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} entries deleted successfully.")

    delete_selected.short_description = "Delete selected entries"
