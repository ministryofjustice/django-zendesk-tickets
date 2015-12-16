from django.conf.urls import url

from .. import views

urlpatterns = [
    url(r'^feedback/$', views.ticket,
        {
            'template_name': 'submit_ticket.html',
            'success_redirect_url': '',
            'subject': 'Test Feedback',
            'tags': ['feedback', 'test']
        }, name='submit_ticket'),
    url(r'^feedback/success$', views.success,
        {
            'template_name': 'success.html',
        }, name='feedback_success'),
]
