
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Ticket
from .forms import TicketForm, TicketUpdateForm, CommentForm, RegisterForm
from django.contrib.auth import logout as auth_logout

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created! Welcome.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('/')

@login_required
def dashboard(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    stats = {
        'total':       tickets.count(),
        'open':        tickets.filter(status='open').count(),
        'in_progress': tickets.filter(status='in_progress').count(),
        'closed':      tickets.filter(status='closed').count(),
    }
    recent = tickets[:5]
    return render(request, 'tickets/dashboard.html', {'stats': stats, 'recent': recent})


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(created_by=request.user)

    status   = request.GET.get('status')
    priority = request.GET.get('priority')
    if status:
        tickets = tickets.filter(status=status)
    if priority:
        tickets = tickets.filter(priority=priority)

    return render(request, 'tickets/ticket_list.html', {
        'tickets':          tickets,
        'current_status':   status,
        'current_priority': priority,
    })


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, created_by=request.user)
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added.')
            return redirect('ticket_detail', pk=pk)

    return render(request, 'tickets/ticket_detail.html', {
        'ticket':       ticket,
        'comments':     ticket.comments.all(),
        'comment_form': comment_form,
    })


@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, 'Ticket submitted successfully!')
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_form.html', {'form': form, 'title': 'New Ticket'})


@login_required
def ticket_update(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = TicketUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket updated.')
            return redirect('ticket_detail', pk=pk)
    else:
        form = TicketUpdateForm(instance=ticket)
    return render(request, 'tickets/ticket_form.html', {'form': form, 'title': 'Edit Ticket'})


@login_required
def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, created_by=request.user)
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Ticket deleted.')
        return redirect('ticket_list')
    return render(request, 'tickets/ticket_confirm_delete.html', {'ticket': ticket})