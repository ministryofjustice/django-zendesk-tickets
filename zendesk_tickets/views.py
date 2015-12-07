from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import TicketForm


def ticket(request,
           template_name=None,
           success_redirect_url='/',
           ticket_template_name='zendesk_tickets/ticket.txt',
           form_class=TicketForm,
           subject='Website Ticket',
           tags=[]):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.submit_ticket(request, subject, tags, ticket_template_name)
            return HttpResponseRedirect(success_redirect_url)
    else:
        form = form_class(
            initial={'referer': request.META.get('HTTP_REFERER')}
        )

    return render(request, template_name, {'form': form})
