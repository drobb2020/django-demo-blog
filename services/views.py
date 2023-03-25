from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TicketFilter, TicketForm
from .models import Ticket


def comments(request):
    context = {}
    return render(request, 'services/comments.html', context)


def cookie(request):
    context = {}
    return render(request, 'services/cookie.html', context)


def copyright(request):
    context = {}
    return render(request, 'services/copyright.html', context)


def dcmapolicy(request):
    context = {}
    return render(request, 'services/dcma_policy.html', context)


def disclaimer(request):
    context = {}
    return render(request, 'services/disclaimer.html', context)


def helpdesk(request):
    context = {}
    return render(request, 'services/helpdesk.html', context)


def postagreement(request):
    context = {}
    return render(request, 'services/member_post_agreement.html', context)


def privacy(request):
    context = {}
    return render(request, 'services/privacy.html', context)


def termsandconditions(request):
    context = {}
    return render(request, 'services/terms_and_conditions.html', context)


def termsofuse(request):
    context = {}
    return render(request, 'services/terms_of_use.html', context)


@login_required
def create_ticket(request):
    if not request.user.is_authenticated:
        return render(request, 'registration/login.html')
    else:
        # (request.POST or None, request.FILES or None) 
        form = TicketForm(request.POST or None)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return render(request, 'services/detail.html', {'ticket': ticket})
        context = {
            'form': form
        }
    return render(request, 'services/create_ticket.html', context)


def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id)
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html')
    else:
        # (request.POST or None, request.FILES or None)
        form = TicketForm(request.POST or None)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return render(request, 'services/detail.html', {'ticket': ticket})
        context = {
            'form': form,
            'title': ticket.title
        }
    return render(request, 'services/create_ticket.html', context)


def detail(request, ticket_id):
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html')
    else:
        user = request.user
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        return render(request, 'services/detail.html', {'ticket': ticket, 'user': user})


def ticket_list(request):
    filter = TicketFilter(request.GET, queryset=Ticket.objects.all())
    return render(request, 'services/helpdesk.html', {'filter': filter})


def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    ticket.delete()
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'services/helpdesk.html', {'tickets': tickets})
