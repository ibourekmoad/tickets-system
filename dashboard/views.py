from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ticket.models import Ticket


# Create your views here.
@login_required
def dashboard(request):
    if request.user.is_customer:
        active_ticket_count = Ticket.objects.filter(customer=request.user, is_resolved=False).count()
        closed_ticket_count = Ticket.objects.filter(customer=request.user, is_resolved=True).count()
        tickets_count = Ticket.objects.filter(customer=request.user).count()
        context = {
            'active_ticket_count': active_ticket_count,
            'closed_ticket_count': closed_ticket_count,
            'tickets_count': tickets_count
        }

        return render(request, 'dashboard/customer_dashboard.html', context)
    elif request.user.is_engineer:
        active_ticket_count = Ticket.objects.filter(engineer=request.user, is_resolved=False).count()
        closed_ticket_count = Ticket.objects.filter(engineer=request.user, is_resolved=True).count()
        tickets_count = Ticket.objects.filter(engineer=request.user).count()
        context = {
            'active_ticket_count': active_ticket_count,
            'closed_ticket_count': closed_ticket_count,
            'tickets_count': tickets_count
        }

        return render(request, 'dashboard/engineer_dashboard.html', context)
    elif request.user.is_superuser:
        return render(request, 'dashboard/admin_dashboard.html')
    else:
        return redirect('logout')
