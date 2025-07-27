from rest_framework import serializers
from .models import User, Conversation, Message


# --- User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()  # Explicit CharField usage

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at',
        ]


# --- Message Serializer ---
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at',
        ]


# --- Conversation Serializer ---
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()  # 👈 Nested manually for flexibility

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages',
        ]

    def get_messages(self, obj):
        messages = obj.messages.all().order_by('sent_at')
        return MessageSerializer(messages, many=True).data


# --- Extra Validation Example (for demonstration) ---
class MessageCreateSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'message_body']

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value
