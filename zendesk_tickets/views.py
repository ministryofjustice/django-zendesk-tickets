import warnings
from urllib.parse import urlparse

from django.core.exceptions import NON_FIELD_ERRORS

try:
    from django.utils.http import url_has_allowed_host_and_scheme
except ImportError:
    from django.utils.http import is_safe_url as url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _
from django.views.generic import FormView, TemplateView
from requests.exceptions import HTTPError

from .forms import TicketForm

RETURN_URL_PARAM = 'next'


def get_safe_return_to(request, return_to):
    """
    Ensure the user-originating redirection url is safe, i.e. within same scheme://domain:port
    """
    if (
        return_to
        and url_has_allowed_host_and_scheme(url=return_to, allowed_hosts=request.get_host())
        and return_to != request.build_absolute_uri()
    ):
        return return_to


class TicketView(FormView):
    form_class = TicketForm
    ticket_subject = _('Website Ticket')
    ticket_template_name = 'zendesk_tickets/ticket.txt'
    ticket_tags = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.return_to = None

    def get(self, request, *args, **kwargs):
        self.return_to = get_safe_return_to(self.request, self.request.META.get('HTTP_REFERER'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['return_to'] = self.return_to
        return super().get_context_data(**kwargs)

    def get_initial(self):
        return dict(referer=self.return_to, **super().get_initial())

    def form_valid(self, form):
        self.return_to = get_safe_return_to(self.request, form.cleaned_data.get('referer'))
        try:
            form.submit_ticket(self.request, self.ticket_subject, self.ticket_tags, self.ticket_template_name)
        except HTTPError:
            form.add_error(NON_FIELD_ERRORS, _('Unexpected error.'))
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        success_url = super().get_success_url()
        if self.return_to:
            return_to = urlparse(self.return_to).path
            success_url = f'{success_url}?{RETURN_URL_PARAM}={return_to}'
        return success_url


class TicketSentView(TemplateView):
    def get_context_data(self, **kwargs):
        kwargs['return_to'] = get_safe_return_to(self.request, self.request.GET.get(RETURN_URL_PARAM))
        return super().get_context_data(**kwargs)


def ticket(request,
           template_name=TicketView.template_name,
           success_redirect_url='/',
           ticket_template_name=TicketView.ticket_template_name,
           form_class=TicketView.form_class,
           subject=TicketView.ticket_subject,
           tags=TicketView.ticket_tags,
           extra_context=None):
    warnings.warn('ticket() view is superseded by class-based TicketView',
                  DeprecationWarning, stacklevel=2)
    init_kwargs = {
        'form_class': form_class,
        'template_name': template_name,
        'success_url': success_redirect_url,
        'ticket_template_name': ticket_template_name,
        'ticket_subject': subject,
        'ticket_tags': tags,
    }
    return TicketView.as_view(**init_kwargs)(request, **(extra_context or {}))


def success(request, template_name=None, extra_context=None):
    warnings.warn('success() view is superseded by class-based TicketSentView',
                  DeprecationWarning, stacklevel=2)
    return TicketSentView.as_view(template_name=template_name)(request, **(extra_context or {}))
