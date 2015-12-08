from unittest import mock
import json

from django.test import SimpleTestCase, RequestFactory, override_settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser

from ..views import ticket


class AssertCalledZendeskPost(object):

    def __init__(self, test_case,
                 expected_url, expected_data, expected_auth, expected_headers):
        self.called = False
        self.test_case = test_case
        self.expected_url = expected_url
        self.expected_data = expected_data
        self.expected_auth = expected_auth
        self.expected_headers = expected_headers

    def __call__(self, url, data, auth, headers):
        self.called = True
        self.test_case.assertEqual(
            url, self.expected_url
        )
        actual_data = json.loads(data)
        self.test_case.assertEqual(
            sorted(actual_data.pop('custom_fields'), key=lambda k: k['id']),
            sorted(self.expected_data.pop('custom_fields'), key=lambda k: k['id'])
        )
        self.test_case.assertEqual(
            actual_data,
            self.expected_data
        )
        self.test_case.assertEqual(
            auth, self.expected_auth
        )
        self.test_case.assertEqual(
            headers, self.expected_headers
        )


@mock.patch('zendesk_tickets.client.requests')
class SubmitFeedbackTestCase(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_referer_is_set_from_header(self, mock_requests):
        response = self.client.get(reverse('submit_ticket'),
                                   HTTP_REFERER='/other/page')
        self.assertEqual('/other/page', response.context['form'].initial['referer'])

    def test_ticket_success(self, mock_requests):
        form_data = {
            'referer': '/other/page',
            'ticket_content': 'The internet is broken.'
        }

        request = self.factory.post(reverse('submit_ticket'), data=form_data)
        request.user = AnonymousUser()
        request.META['HTTP_USER_AGENT'] = 'test_client'

        mock_requests.post.side_effect = AssertCalledZendeskPost(
            self,
            'https://test.notzendesk.com/api/v2/tickets.json',
            ({'subject': 'Website Ticket', 'tags': ['test'],
             'group_id': 222222,
             'comment': {'body': 'The internet is broken.'},
             'requester_id': 111111, 'custom_fields':
             [{'id': 32, 'value': 'Anonymous'}, {'id': 31, 'value': '/other/page'},
              {'id': 33, 'value': 'test_client'}]}),
            ('zendesk_user/token', 'api_token'),
            {'content-type': 'application/json'}
        )

        ticket(request, template_name='submit_ticket.html', tags=['test'])

        self.assertTrue(mock_requests.post.side_effect.called)

    @override_settings(ZENDESK_CUSTOM_FIELDS={})
    def test_no_custom_fields_included_if_not_defined(self, mock_requests):
        form_data = {
            'referer': '/other/page',
            'ticket_content': 'The internet is broken.'
        }

        request = self.factory.post(reverse('submit_ticket'), data=form_data)
        request.user = AnonymousUser()
        request.META['HTTP_USER_AGENT'] = 'test_client'

        mock_requests.post.side_effect = AssertCalledZendeskPost(
            self,
            'https://test.notzendesk.com/api/v2/tickets.json',
            ({'subject': 'Website Ticket', 'tags': ['test'],
             'group_id': 222222,
             'comment': {'body': 'The internet is broken.'},
             'requester_id': 111111, 'custom_fields': []}),
            ('zendesk_user/token', 'api_token'),
            {'content-type': 'application/json'}
        )

        ticket(request, template_name='submit_ticket.html', tags=['test'])

        self.assertTrue(mock_requests.post.side_effect.called)
