from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField(read_only=True)
    recipient = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "recipient", "actor", "verb", "target_object_id", "timestamp", "is_read"]
