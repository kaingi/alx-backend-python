from django.db import models
from django.contrib.auth.models import User

def unread_inbox(request):
    user = request.user
    unread_messages = Message.unread.unread_for_user(user) \
        .select_related('sender') \
        .only('id', 'sender__id', 'sender__username', 'content', 'timestamp')
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='edited_messages')  # <-- Add this line
    read = models.BooleanField(default=False)


     # Attach the custom manager
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager for unread messages

    parent_message = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"
class MessageHistory(models.Model):

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    