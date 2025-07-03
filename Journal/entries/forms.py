from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'content', 'tags']

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

        labels = {
            'title': 'Title',
            'content': 'Content',
            'tags': 'Tags',
        }

        """help_texts = {
            'title': 'Enter the title of the entry',
            'content': 'Enter the content of the entry',
            'tags': 'Select the tags for the entry',
        }"""

        error_messages = {
            'title': {
                'required': 'Please enter a title for the entry',
            },
            'content': {
                'required': 'Please enter content for the entry',
            },
        }

        def __init__(self, *args, **kwargs):
            super(EntryForm, self).__init__(*args, **kwargs)
            self.fields['tags'].queryset = self.fields['tags'].queryset.order_by('name')

        def save(self, commit=True):
            entry = super(EntryForm, self).save(commit=False)
            if commit:
                entry.save()
            return entry

class UpdateEntryForm(EntryForm):
    def __init__(self, *args, **kwargs):
        super(UpdateEntryForm, self).__init__(*args, **kwargs)
        self.fields['tags'].queryset = self.fields['tags'].queryset.order_by('name')