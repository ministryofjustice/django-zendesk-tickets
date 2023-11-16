import json
from unittest import mock

from django.contrib.auth.models import AnonymousUser
from django.test import SimpleTestCase, RequestFactory, override_settings
from django.urls import reverse

from zendesk_tickets.views import ticket


class AssertCalledZendeskPost:
    def __init__(self, test_case, expected_url, expected_data, expected_auth, expected_headers):
        self.called = False
        self.test_case = test_case
        self.expected_url = expected_url
        self.expected_data = expected_data
        self.expected_auth = expected_auth
        self.expected_headers = expected_headers

    def __call__(self, url, data, auth, headers):
        self.called = True
        self.test_case.assertEqual(
            url, self.expected_url,
        )
        actual_data = json.loads(data)
        self.test_case.assertEqual(
            sorted(actual_data['ticket'].pop('custom_fields'), key=lambda k: k['id']),
            sorted(self.expected_data['ticket'].pop('custom_fields'), key=lambda k: k['id'])
        )
        self.test_case.assertEqual(
            actual_data,
            self.expected_data,
        )
        self.test_case.assertEqual(
            auth, self.expected_auth,
        )
        self.test_case.assertEqual(
            headers, self.expected_headers,
        )
        return mock.MagicMock()


@mock.patch('zendesk_tickets.client.requests')
class SubmitFeedbackTestCase(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_referer_is_set_from_header(self, _):
        response = self.client.get(reverse('submit_ticket'), HTTP_REFERER='/other/page')
        self.assertEqual('/other/page', response.context['form'].initial['referer'])

    def test_ticket_success(self, mock_requests):
        form_data = {
            'referer': '/other/page',
            'ticket_content': 'The internet is broken.',
        }

        request = self.factory.post(reverse('submit_ticket'), data=form_data)
        request.user = AnonymousUser()
        request.META['HTTP_USER_AGENT'] = 'test_client'

        mock_requests.post.side_effect = AssertCalledZendeskPost(
            self,
            'https://zendesk.local/api/v2/tickets.json',
            {'ticket': {'subject': 'Website Ticket', 'tags': ['test'],
                        'group_id': 222222,
                        'comment': {'body': 'The internet is broken.'},
                        'requester_id': 111111,
                        'custom_fields': [{'id': 32, 'value': 'Anonymous'},
                                          {'id': 31, 'value': '/other/page'},
                                          {'id': 33, 'value': 'test_client'}]}},
            ('zendesk_user/token', 'api_token'),
            {'content-type': 'application/json'}
        )

        ticket(request, template_name='submit_ticket.html', tags=['test'])

        self.assertTrue(mock_requests.post.side_effect.called)

    def test_ticket_success_with_user(self, mock_requests):
        form_data = {
            'referer': '/other/page',
            'ticket_content': 'The internet is broken.',
        }

        request = self.factory.post(reverse('submit_ticket'), data=form_data)
        request.user = mock.MagicMock()
        request.user.username = 'TestUser'
        request.user.email = 'test@user.com'
        request.META['HTTP_USER_AGENT'] = 'test_client'

        mock_requests.post.side_effect = AssertCalledZendeskPost(
            self,
            'https://zendesk.local/api/v2/tickets.json',
            {'ticket': {'subject': 'Website Ticket', 'tags': ['test'],
                        'group_id': 222222,
                        'comment': {'body': 'The internet is broken.'},
                        'requester': {'name': 'Sender: test',
                                      'email': 'test@user.com'},
                        'custom_fields': [{'id': 32, 'value': 'TestUser'},
                                          {'id': 31, 'value': '/other/page'},
                                          {'id': 33, 'value': 'test_client'}]}},
            ('zendesk_user/token', 'api_token'),
            {'content-type': 'application/json'}
        )

        ticket(request, template_name='submit_ticket.html', tags=['test'])

        self.assertTrue(mock_requests.post.side_effect.called)

    def test_ticket_success_with_contact_email(self, mock_requests):
        form_data = {
            'referer': '/other/page',
            'ticket_content': 'Here is some feedback.\n  <script>alert("hello ");</script>  \n',
            'contact_email': 'example@example.com',
        }

        mock_requests.post.side_effect = AssertCalledZendeskPost(
            self,
            'https://zendesk.local/api/v2/tickets.json',
            {'ticket': {'subject': 'Test Feedback with email address',
                        'tags': ['feedback', 'test', 'with-email'],
                        'group_id': 222222,
                        'comment': {'body': 'Here is some feedback.\n  <script>alert("hello ");</script>'},
                        'requester': {'name': 'Sender: example',
                                      'email': 'example@example.com'},
                        'custom_fields': [{'id': 32, 'value': 'Anonymous'},
                                          {'id': 31, 'value': '/other/page'},
                                          {'id': 33, 'value': 'test_client'},
                                          {'id': 34, 'value': 'example@example.com'}]}},
            ('zendesk_user/token', 'api_token'),
            {'content-type': 'application/json'}
        )

        self.client.post(reverse('submit_ticket_with_email'), data=form_data,
                         HTTP_USER_AGENT='test_client')
        self.assertTrue(mock_requests.post.side_effect.called)

    def test_ticket_success_provides_next_to_redirect(self, _):
        form_data = {
            'referer': '/other/page',
            'ticket_content': 'The internet is broken.',
        }

        request = self.factory.post(reverse('submit_ticket'), data=form_data)
        request.user = AnonymousUser()
        request.META['HTTP_USER_AGENT'] = 'test_client'

        response = ticket(request, template_name='submit_ticket.html', tags=['test'])
        self.assertEqual(response.url, '/?next=/other/page')

    def test_success_adds_next_to_context(self, _):
        response = self.client.get(reverse('feedback_success'),
                                   {'next': '/other/page'})
        self.assertEqual(response.context['return_to'], '/other/page')

    def test_dodgy_next_not_used(self, _):
        response = self.client.get(reverse('feedback_success'),
                                   {'next': 'https://www.phishing.com'})
        self.assertEqual(response.context['return_to'], None)

    def test_no_username_attr_handled(self, mock_requests):
        form_data = {
            'referer': '/other/page',
            'ticket_content': 'The internet is broken.',
        }

        request = self.factory.post(reverse('submit_ticket'), data=form_data)
        # set user object with no username attribute
        request.user = object()
        request.META['HTTP_USER_AGENT'] = 'test_client'

        mock_requests.post.side_effect = AssertCalledZendeskPost(
            self,
            'https://zendesk.local/api/v2/tickets.json',
            {'ticket': {'subject': 'Website Ticket', 'tags': ['test'],
                        'group_id': 222222,
                        'comment': {'body': 'The internet is broken.'},
                        'requester_id': 111111,
                        'custom_fields': [{'id': 32, 'value': 'Anonymous'},
                                          {'id': 31, 'value': '/other/page'},
                                          {'id': 33, 'value': 'test_client'}]}},
            ('zendesk_user/token', 'api_token'),
            {'content-type': 'application/json'}
        )

        ticket(request, template_name='submit_ticket.html', tags=['test'])

        self.assertTrue(mock_requests.post.side_effect.called)

    @override_settings(ZENDESK_CUSTOM_FIELDS={})
    def test_no_custom_fields_included_if_not_defined(self, mock_requests):
        form_data = {
            'referer': '/other/page',
            'ticket_content': 'The internet is broken.',
        }

        request = self.factory.post(reverse('submit_ticket'), data=form_data)
        request.user = AnonymousUser()
        request.META['HTTP_USER_AGENT'] = 'test_client'

        mock_requests.post.side_effect = AssertCalledZendeskPost(
            self,
            'https://zendesk.local/api/v2/tickets.json',
            {'ticket': {'subject': 'Website Ticket', 'tags': ['test'],
                        'group_id': 222222,
                        'comment': {'body': 'The internet is broken.'},
                        'requester_id': 111111, 'custom_fields': []}},
            ('zendesk_user/token', 'api_token'),
            {'content-type': 'application/json'}
        )

        ticket(request, template_name='submit_ticket.html', tags=['test'])

        self.assertTrue(mock_requests.post.side_effect.called)
