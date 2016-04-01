from django.conf.urls import url

from .. import forms, views

urlpatterns = [
    url(r'^feedback/$', views.ticket,
        {
            'template_name': 'submit_ticket.html',
            'success_redirect_url': '',
            'subject': 'Test Feedback',
            'tags': ['feedback', 'test']
        }, name='submit_ticket'),
    url(r'^feedback-with-email/$', views.ticket,
        {
            'form_class': forms.EmailTicketForm,
            'template_name': 'submit_ticket.html',
            'success_redirect_url': '',
            'subject': 'Test Feedback with email address',
            'tags': ['feedback', 'test', 'with-email']
        }, name='submit_ticket_with_email'),
    url(r'^feedback/success$', views.success,
        {
            'template_name': 'success.html',
        }, name='feedback_success'),
]
