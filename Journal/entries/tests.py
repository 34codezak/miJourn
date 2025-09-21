from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Entry, Tag
from .serializers import EntriesSerializer


class EntriesSerializerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="journaler", password="test-pass"
        )
        self.tag_a = Tag.objects.create(name="Work")
        self.tag_b = Tag.objects.create(name="Personal")
        self.entry = Entry.objects.create(
            user=self.user,
            title="Daily reflection",
            content="Thoughts about the day.",
        )
        self.entry.tags.add(self.tag_a, self.tag_b)

    def test_serializes_entry_with_tags(self):
        serializer = EntriesSerializer(self.entry)

        self.assertEqual(serializer.data["user"], self.user.username)
        self.assertEqual(serializer.data["tags"], ["Work", "Personal"])

    def test_update_ignores_tags_field(self):
        serializer = EntriesSerializer(
            instance=self.entry,
            data={
                "title": "Updated reflection",
                "content": "Updated thoughts.",
                "tags": ["Work"],
            },
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_entry = serializer.save()

        self.assertNotIn("tags", serializer.validated_data)
        updated_entry.refresh_from_db()
        self.assertEqual(updated_entry.title, "Updated reflection")
        self.assertEqual(updated_entry.content, "Updated thoughts.")
        self.assertCountEqual(
            updated_entry.tags.values_list("name", flat=True), ["Work", "Personal"]
        )
