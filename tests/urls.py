from django.conf.urls import url
from django.urls import reverse_lazy

from zendesk_tickets import forms, views

urlpatterns = [
    # class-based views
    url(r'^ticket/$', views.TicketView.as_view(
        success_url=reverse_lazy('ticket_sent'),
        template_name='submit_ticket.html',
        ticket_subject='Test Feedback',
        ticket_tags=['feedback', 'test'],
    ), name='ticket'),
    url(r'^ticket-with-email/$', views.TicketView.as_view(
        form_class=forms.EmailTicketForm,
        success_url=reverse_lazy('ticket_sent'),
        template_name='submit_ticket.html',
        ticket_subject='Test Feedback with email address',
        ticket_tags=['feedback', 'test', 'with-email'],
    ), name='ticket_with_email'),
    url(r'^ticket/sent/$', views.TicketSentView.as_view(
        template_name='success.html',
    ), name='ticket_sent'),

    # deprecated function views
    url(r'^feedback/$', views.ticket,
        {
            'template_name': 'submit_ticket.html',
            'success_redirect_url': '/',
            'subject': 'Test Feedback',
            'tags': ['feedback', 'test']
        }, name='submit_ticket'),
    url(r'^feedback-with-email/$', views.ticket,
        {
            'form_class': forms.EmailTicketForm,
            'template_name': 'submit_ticket.html',
            'success_redirect_url': '/',
            'subject': 'Test Feedback with email address',
            'tags': ['feedback', 'test', 'with-email']
        }, name='submit_ticket_with_email'),
    url(r'^feedback/success$', views.success,
        {
            'template_name': 'success.html',
        }, name='feedback_success'),
]
