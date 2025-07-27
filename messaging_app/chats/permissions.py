from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to view/send/update/delete messages.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the object is a message or conversation and if the user is a participant
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False