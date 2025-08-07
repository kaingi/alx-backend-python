from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.views.decorators.cache import cache_page

@cache_page(60)  # cache timeout in seconds
def messages_list(request):
    # Your normal view logic
    messages = Message.objects.all().select_related('sender', 'receiver')
    return render(request, 'messages/list.html', {'messages': messages})
@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('login')  # Or any other page after deletion

def unread_inbox(request):
    user = request.user
    unread_messages = Message.unread.unread_for_user(user).select_related('sender')
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})

def get_replies(message):
    # Use select_related to get sender and receiver efficiently on replies
    replies = message.replies.select_related('sender', 'receiver').all()
    result = []
    for reply in replies:
        result.append({
            'message': reply,
            'replies': get_replies(reply)  # recursive call
        })
    return result

def threaded_messages_view(request):
    # Get top-level messages involving the user
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related('replies')

    # Build a threaded structure
    threaded = []
    for msg in messages:
        threaded.append({
            'message': msg,
            'replies': get_replies(msg)
        })

    return render(request, 'messaging/threaded_messages.html', {'threaded_messages': threaded})

def user_conversations(request):
    # Filter messages where the user is either sender or receiver
    messages = Message.objects.filter(
        models.Q(sender=request.user) | models.Q(receiver=request.user),
        parent_message__isnull=True  # only top-level messages
    ).select_related('sender', 'receiver') \
     .prefetch_related('replies__sender', 'replies__receiver')

    return render(request, 'messaging/conversations.html', {'messages': messages})