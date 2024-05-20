import random
import string

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .form import TicketCreationForm, AssignTicketForm
from .models import Ticket

User = get_user_model()


# create ticket
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketCreationForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.customer = request.user
            while not var.ticket_id:
                id = ''.join(random.choices(string.digits, k=6))
                try:
                    var.ticket_id = id
                    var.save()
                    # email to cx
                    subject = f'{var.ticket_title} - {var.ticket_id}'
                    message = 'Thank you for creating a new ticket we will assign an engineer soon.'
                    email_from = 'moad.ibourek121@gmail.com'
                    receiver_list = [request.user.email, ]
                    send_mail(subject, message, email_from, receiver_list)
                    messages.success(request, 'Ticket successfully created!')
                    return redirect('customer-active-ticket')
                except IntegrityError:
                    continue
        else:
            messages.warning(request, 'Please check the form input')
            return redirect('create_ticket')
    else:
        form = TicketCreationForm()
        context = {'form': form}
        return render(request, 'ticket/create_ticket.html', context)


# see the tickets created by a customer
def customer_active_ticket(request):
    tickets = Ticket.objects.filter(customer=request.user, is_resolved=False).order_by('-created_at')
    context = {'tickets': tickets}
    return render(request, 'ticket/customer_active_tickets.html', context)


# see the tickets created by a customer resolved
def customer_resolved_ticket(request):
    tickets = Ticket.objects.filter(customer=request.user, is_resolved=True).order_by('-created_at')
    context = {'tickets': tickets}
    return render(request, 'ticket/customer_resolved_tickets.html', context)


# engineer see the tickets  active
def engineer_active_ticket(request):
    tickets = Ticket.objects.filter(engineer=request.user, is_resolved=False).order_by('-created_at')
    context = {'tickets': tickets}
    return render(request, 'ticket/engineer_active_tickets.html', context)


# engineer see the tickets  resolved
def engineer_resolved_ticket(request):
    tickets = Ticket.objects.filter(engineer=request.user, is_resolved=True).order_by('-created_at')
    context = {'tickets': tickets}
    return render(request, 'ticket/engineer_resolved_tickets.html', context)


# assign a ticket to engineer
def assign_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        form = AssignTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_assigned = True
            var.status = 'Active'
            var.save()
            messages.success(request, f'Ticket successfully assigned to {var.engineer}')
            return redirect('queue-ticket')
        else:
            messages.warning(request, 'Please check the form input')
            return redirect('assign_ticket')
    else:
        form = AssignTicketForm(instance=ticket)
        context = {'form': form, ticket: 'ticket'}
        return render(request, 'ticket/assign_ticket.html', context)


# get ticket details
def ticket_detail(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    context = {'ticket': ticket}
    return render(request, 'ticket/detail_ticket.html', context)


# ticket queue (only for admins)
def ticket_queue(request):
    tickets = Ticket.objects.filter(is_assigned=False)
    context = {'tickets': tickets}
    return render(request, 'ticket/queue_ticket.html', context)


def resolve_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    if request.method == 'POST':
        rs = request.POST.get('resolution_steps')
        ticket.resolution_steps = rs
        ticket.is_resolved = True
        ticket.status = 'Resolved'
        ticket.save()
        messages.success(request, 'Ticket successfully Resolved')
        return redirect('dashboard')
