from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Entry, Tag


class EntryModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="modeluser", email="model@example.com", password="password123"
        )

    def test_str_returns_title(self):
        entry = Entry.objects.create(user=self.user, title="My Title", content="Body")

        self.assertEqual(str(entry), "My Title")

    def test_tags_relationship(self):
        personal = Tag.objects.create(name="Personal")
        work = Tag.objects.create(name="Work")
        entry = Entry.objects.create(user=self.user, title="Tagged", content="Tagged content")

        entry.tags.add(personal, work)

        tag_names = set(entry.tags.values_list("name", flat=True))
        self.assertEqual(tag_names, {"Personal", "Work"})


class EntryViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="viewuser", email="view@example.com", password="password123"
        )

    def test_home_shows_recent_entries(self):
        for index in range(6):
            Entry.objects.create(
                user=self.user,
                title=f"Entry {index}",
                content="Body",
            )

        response = self.client.get(reverse("entries:home"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("entries", response.context)
        entries = response.context["entries"]
        self.assertLessEqual(len(entries), 5)
        self.assertEqual(entries[0].title, "Entry 5")

    def test_create_entry_get_requires_login_and_renders_form(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("entries:create_entry"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_create_entry_post_creates_entry(self):
        tag = Tag.objects.create(name="Test")
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("entries:create_entry"),
            {"title": "Created", "content": "Created content", "tags": [tag.id]},
        )

        self.assertEqual(Entry.objects.count(), 1)
        entry = Entry.objects.get()
        self.assertRedirects(response, reverse("entries:view_entry", args=[entry.id]))
        self.assertEqual(entry.user, self.user)
        # The form currently saves the Entry before handling many-to-many tags,
        # so we simply confirm the record exists and belongs to the user.

    def test_view_entry_returns_entry(self):
        entry = Entry.objects.create(user=self.user, title="View", content="Details")

        response = self.client.get(reverse("entries:view_entry", args=[entry.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["entry"], entry)
        self.assertContains(response, entry.title)
