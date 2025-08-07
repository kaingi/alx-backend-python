from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class SignalTestCase(TestCase):
    def test_notification_created(self):
        sender = User.objects.create_user(username='sender', password='123')
        receiver = User.objects.create_user(username='receiver', password='456')

        msg = Message.objects.create(sender=sender, receiver=receiver, content="Hello")

        self.assertEqual(Notification.objects.count(), 1)
        note = Notification.objects.first()
        self.assertEqual(note.user, receiver)
        self.assertEqual(note.message, msg)
