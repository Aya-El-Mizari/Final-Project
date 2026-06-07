from rest_framework import serializers
from .models import Ticket, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model  = Comment
        fields = ['id', 'author', 'body', 'created_at']
        read_only_fields = ['created_at']


class TicketSerializer(serializers.ModelSerializer):
    created_by  = serializers.StringRelatedField(read_only=True)
    assigned_to = serializers.StringRelatedField(read_only=True)
    comments    = CommentSerializer(many=True, read_only=True)

    class Meta:
        model  = Ticket
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'created_by', 'assigned_to', 'comments',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']