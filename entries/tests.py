from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Entry


class EntryPermissionsTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username='alice',
            password='password123',
        )
        self.other_user = user_model.objects.create_user(
            username='bob',
            password='password123',
        )

        self.entry = Entry.objects.create(
            user=self.user,
            title='Alice Entry',
            content='Shared content keyword',
        )
        self.other_entry = Entry.objects.create(
            user=self.other_user,
            title='Bob Entry',
            content='Shared content keyword',
        )

    def test_view_entry_other_user_returns_404(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse('entries:view_entry', args=[self.other_entry.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_view_all_entries_only_returns_user_entries(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('entries:view_all_entries'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['entries']), [self.entry])

    def test_search_entries_excludes_other_users_entries(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse('entries:search_entries'),
            {'query': 'shared'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['results']), [self.entry])

    def test_delete_entry_other_user_returns_404(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('entries:delete_entry', args=[self.other_entry.id])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Entry.objects.filter(id=self.other_entry.id).exists())

    def test_multi_delete_cannot_remove_other_users_entries(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('entries:multi_delete'),
            {'selections': [self.entry.id, self.other_entry.id]},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Entry.objects.filter(id=self.other_entry.id).exists())
        self.assertTrue(Entry.objects.filter(id=self.entry.id).exists())
