from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Ticket, Comment
from .serializers import TicketSerializer, CommentSerializer


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class   = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Regular users see only their tickets
        # Staff see all tickets
        if self.request.user.is_staff:
            return Ticket.objects.all().select_related('created_by', 'assigned_to')
        return Ticket.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Quick action to close a ticket."""
        ticket = self.get_object()
        ticket.status = 'closed'
        ticket.save()
        return Response({'status': 'ticket closed'})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Returns ticket counts by status."""
        tickets = self.get_queryset()
        return Response({
            'total':       tickets.count(),
            'open':        tickets.filter(status='open').count(),
            'in_progress': tickets.filter(status='in_progress').count(),
            'closed':      tickets.filter(status='closed').count(),
        })


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class   = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(ticket_id=self.kwargs['ticket_pk'])

    def perform_create(self, serializer):
        ticket = Ticket.objects.get(pk=self.kwargs['ticket_pk'])
        serializer.save(author=self.request.user, ticket=ticket)