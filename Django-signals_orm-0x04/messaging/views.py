from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('login')  # Or any other page after deletion


def threaded_conversations(request):
    messages = Message.objects.filter(parent_message__isnull=True).prefetch_related('message_set')
    return render(request, 'threaded.html', {'messages': messages})