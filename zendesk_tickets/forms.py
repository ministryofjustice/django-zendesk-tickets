from django import forms
from django.conf import settings
from django.template import loader, Context
from django.utils.translation import ugettext as _

from . import client


class BaseTicketForm(forms.Form):
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

    def submit_ticket(self, request, subject, tags,
                      ticket_template_name, extra_context={}):
        context = Context(dict(self.cleaned_data, **extra_context))
        body = loader.get_template(ticket_template_name).render(context)

        client.create_ticket(
            subject,
            tags,
            body,
            self._populate_custom_fields(context)
        )


class TicketForm(BaseTicketForm):
    ticket_content = forms.CharField(
        label=_('Please enter any feedback that you have'),
        widget=forms.Textarea
    )

    def submit_ticket(self, request, subject, tags,
                      ticket_template_name, extra_context={}):
        extra_context = dict(extra_context, **{
            'username': getattr(request.user, 'username', 'Anonymous'),
            'user_agent': request.META.get('HTTP_USER_AGENT')
        })

        super().submit_ticket(request, subject, tags,
                              ticket_template_name, extra_context)
