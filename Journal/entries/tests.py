from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .forms import MultiDeleteForm
from .models import Entry


class MultiDeleteViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='tester', password='testpass123'
        )

    def test_get_renders_multi_delete_form(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('entries:multi_delete'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], MultiDeleteForm)

    def test_post_deletes_selected_entries_and_sets_message(self):
        self.client.force_login(self.user)
        entry_one = Entry.objects.create(
            user=self.user, title='Entry One', content='Content One'
        )
        entry_two = Entry.objects.create(
            user=self.user, title='Entry Two', content='Content Two'
        )

        response = self.client.post(
            reverse('entries:multi_delete'),
            {'selections': [entry_one.pk, entry_two.pk]},
            follow=True,
        )

        self.assertRedirects(response, reverse('entries:view_all_entries'))
        self.assertFalse(
            Entry.objects.filter(pk__in=[entry_one.pk, entry_two.pk]).exists()
        )
        messages = [message.message for message in get_messages(response.wsgi_request)]
        self.assertIn('Deleted 2 entries successfully.', messages)
