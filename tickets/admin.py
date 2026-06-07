from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Ticket, Comment

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display  = ['title', 'status', 'priority', 'created_by', 'created_at']
    list_filter   = ['status', 'priority']
    search_fields = ['title', 'description']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'author', 'created_at']