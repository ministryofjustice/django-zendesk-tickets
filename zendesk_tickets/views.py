from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _
from requests.exceptions import HTTPError
from six.moves.urllib.parse import urlparse

from .forms import TicketForm

RETURN_URL_FIELD = 'next'


def get_safe_return_to(request, return_to):
    # Ensure the user-originating redirection url is safe.
    if not return_to or not is_safe_url(url=return_to, host=request.get_host()):
        return None
    return return_to


def ticket(request,
           template_name=None,
           success_redirect_url='/',
           ticket_template_name='zendesk_tickets/ticket.txt',
           form_class=TicketForm,
           subject='Website Ticket',
           tags=[],
           extra_context=None):
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            return_to = get_safe_return_to(request, form.cleaned_data.get('referer'))
            try:
                form.submit_ticket(request, subject, tags, ticket_template_name)
                if return_to:
                    return_to = urlparse(return_to).path
                    success_redirect_url = (
                        success_redirect_url +
                        ('?%s=%s' % (RETURN_URL_FIELD, return_to))
                    )
                return HttpResponseRedirect(success_redirect_url)
            except HTTPError:
                form.add_error(NON_FIELD_ERRORS, _('Unexpected error.'))
        else:
            return_to = get_safe_return_to(request, request.POST.get('referer'))
    else:
        return_to = get_safe_return_to(request, request.META.get('HTTP_REFERER'))
        form = form_class(
            initial={'referer': return_to}
        )

    context = {'form': form, 'return_to': return_to}
    if extra_context:
        context.update(extra_context)
    return render(request, template_name, context=context)


def success(request, template_name=None, extra_context=None):
    return_to = get_safe_return_to(request, request.GET.get(RETURN_URL_FIELD))
    context = {'return_to': return_to}
    if extra_context:
        context.update(extra_context)
    return render(request, template_name, context=context)
