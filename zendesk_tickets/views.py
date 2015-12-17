from urllib.parse import urlparse

from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _
from requests.exceptions import HTTPError

from .forms import TicketForm

RETURN_URL_FIELD = 'next'


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
            try:
                form.submit_ticket(request, subject, tags, ticket_template_name)
                referer = form.cleaned_data.get('referer')
                if referer:
                    come_from = urlparse(referer).path
                    success_redirect_url = (
                        success_redirect_url +
                        ('?%s=%s' % (RETURN_URL_FIELD, come_from))
                    )
                return HttpResponseRedirect(success_redirect_url)
            except HTTPError:
                form.add_error(NON_FIELD_ERRORS, _('Unexpected error.'))
    else:
        form = form_class(
            initial={'referer': request.META.get('HTTP_REFERER')}
        )

    return render(request, template_name, {'form': form})


def success(request, template_name=None):
    return_to = request.GET.get(RETURN_URL_FIELD)

    # Ensure the user-originating redirection url is safe.
    if not return_to or not is_safe_url(url=return_to, host=request.get_host()):
        return_to = None

    return TemplateResponse(request, template_name, {'return_to': return_to})
