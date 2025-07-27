from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of the conversation.
    """

    def has_permission(self, request, view):
        # Only authenticated users can proceed
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Determine the conversation object from either a Message or a Conversation
        if hasattr(obj, 'participants'):  # Conversation instance
            participants = obj.participants.all()
        elif hasattr(obj, 'conversation'):  # Message instance
            participants = obj.conversation.participants.all()
        else:
            return False

        # Check if the user is one of the participants
        if user not in participants:
            return False

        # Allow GET, POST, PUT, PATCH, DELETE for participants only
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return True

        # Default deny
        return False
