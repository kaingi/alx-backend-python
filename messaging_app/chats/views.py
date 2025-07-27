from rest_framework import permissions, viewsets
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
mission_classes = [permissions.IsAuthenticated, IsOwner]
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.response import Response

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participant_ids', [])
        if not participant_ids or len(participant_ids) < 2:
            return Response(
                {"error": "At least two participants are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response(
                {"error": "Some user_ids are invalid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class MessageViewSet(viewsets.ModelViewSet):
    qpermission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    ...

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'detail': 'Conversation not found.'}, status=HTTP_404_NOT_FOUND)

        if request.user not in conversation.participants.all():
            return Response({'detail': 'You are not a participant of this conversation.'}, status=HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)