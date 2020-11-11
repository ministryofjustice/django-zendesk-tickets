from django import forms
from django.conf import settings
from django.template import loader
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy as _

from . import client


class BaseTicketForm(forms.Form):
    """
    Base feedback form, only collects HTTP referrer
    """
    referer = forms.CharField(widget=forms.HiddenInput, required=False)

    def _populate_custom_fields(self, context):
        fields = []
        for custom_field in settings.ZENDESK_CUSTOM_FIELDS:
            value = context.get(custom_field)
            if value is not None:
                fields.append({
                    'id': settings.ZENDESK_CUSTOM_FIELDS[custom_field],
                    'value': value
                })
        return fields

    def submit_ticket(self, request, subject, tags, ticket_template_name, requester_email=None, extra_context=None):
        extra_context = extra_context or {}
        subject = force_text(subject)
        tags = list(map(force_text, tags))
        context = dict(self.cleaned_data, **extra_context)
        context = {
            key: force_text(value, strings_only=True)
            for key, value in context.items()
        }
        body = loader.get_template(ticket_template_name).render(context).strip()

        client.create_ticket(
            subject,
            tags,
            body,
            requester_email=requester_email,
            custom_fields=self._populate_custom_fields(context)
        )


class TicketForm(BaseTicketForm):
    """
    Simple feedback form
    """
    ticket_content = forms.CharField(
        label=_('Enter your feedback or any questions you have about this service.'),
        widget=forms.Textarea
    )

    def submit_ticket(self, request, subject, tags, ticket_template_name, requester_email=None, extra_context=None):
        extra_context = extra_context or {}
        extra_context = dict(extra_context, **{
            'username': getattr(request.user, 'username', None) or _('Anonymous'),
            'user_agent': request.META.get('HTTP_USER_AGENT')
        })
        if not requester_email:
            requester_email = getattr(request.user, 'email', None)
        return super().submit_ticket(request, subject, tags, ticket_template_name, requester_email, extra_context)


class EmailTicketForm(TicketForm):
    """
    Feedback form that also allows entering an email address
    """
    contact_email = forms.EmailField(
        label=_('Your email address'), required=False
    )

    def submit_ticket(self, request, subject, tags, ticket_template_name, requester_email=None, extra_context=None):
        extra_context = extra_context or {}
        if not requester_email:
            requester_email = self.cleaned_data['contact_email']
        return super().submit_ticket(request, subject, tags, ticket_template_name, requester_email, extra_context)
