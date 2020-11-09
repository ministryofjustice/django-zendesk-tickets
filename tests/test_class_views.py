import json
from unittest import mock

from django.test import RequestFactory, SimpleTestCase, override_settings
from django.urls import resolve, reverse


@mock.patch('zendesk_tickets.client.requests')
class TicketViewTestCase(SimpleTestCase):
    def assertPostedToZendesk(self, mock_requests, ticket_data):  # noqa
        self.assertEqual(mock_requests.post.call_count, 1)
        args, kwargs = mock_requests.post.call_args
        kwargs['data'] = json.loads(kwargs['data'])
        kwargs['data']['ticket']['custom_fields'] = sorted(kwargs['data']['ticket']['custom_fields'],
                                                           key=lambda field: field['id'])
        ticket_data['custom_fields'] = sorted(ticket_data['custom_fields'],
                                              key=lambda field: field['id'])
        self.assertSequenceEqual(args, ('https://zendesk.local/api/v2/tickets.json',))
        self.assertDictEqual(kwargs, dict(
            data={'ticket': ticket_data},
            auth=('zendesk_user/token', 'api_token'),
            headers={'content-type': 'application/json'},
        ))

    def test_referer_is_prepopulated(self, mock_requests):
        response = self.client.get(reverse('ticket'))
        self.assertIsNone(response.context['form'].initial['referer'])

        response = self.client.get(reverse('ticket'), HTTP_REFERER='/other/page')
        self.assertEqual('/other/page', response.context['form'].initial['referer'])

        mock_requests.post.assert_not_called()

    def test_submission_failing_if_no_ticket_content(self, mock_requests):
        response = self.client.post(reverse('ticket'), data={})
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertFormError(response, 'form', 'ticket_content', errors=['This field is required.'])
        mock_requests.post.assert_not_called()

    def test_anonymous_submission_shows_sent_page(self, mock_requests):
        response = self.client.post(reverse('ticket'), data={
            'ticket_content': 'The site is broken',
        }, HTTP_USER_AGENT='test_client')
        self.assertRedirects(response, reverse('ticket_sent'))
        self.assertPostedToZendesk(mock_requests, {
            'subject': 'Test Feedback',
            'comment': {'body': 'The site is broken'},
            'tags': ['feedback', 'test'],
            'group_id': 222222,
            'requester_id': 111111,
            'custom_fields': [{'id': 32, 'value': 'Anonymous'},
                              {'id': 31, 'value': ''},
                              {'id': 33, 'value': 'test_client'}],
        })

    def test_authenticated_submission_shows_sent_page(self, mock_requests):
        request = RequestFactory().post(reverse('ticket'), data={
            'ticket_content': 'The site is broken',
        })
        request.user = mock.MagicMock()
        request.user.username = 'TestUser'
        request.user.email = 'test@user.com'
        request.META['HTTP_USER_AGENT'] = 'test_client'
        match = resolve(reverse('ticket'))
        response = match.func(request)
        response.client = self.client
        self.assertRedirects(response, reverse('ticket_sent'))
        self.assertPostedToZendesk(mock_requests, {
            'subject': 'Test Feedback',
            'comment': {'body': 'The site is broken'},
            'tags': ['feedback', 'test'],
            'group_id': 222222,
            'requester': {'name': 'Sender: test',
                          'email': 'test@user.com'},
            'custom_fields': [{'id': 32, 'value': 'TestUser'},
                              {'id': 31, 'value': ''},
                              {'id': 33, 'value': 'test_client'}],
        })

    def test_authenticated_submission_with_custom_user_shows_sent_page(self, mock_requests):
        request = RequestFactory().post(reverse('ticket'), data={
            'ticket_content': 'The site is broken',
        })
        request.user = object()
        request.META['HTTP_USER_AGENT'] = 'test_client'
        match = resolve(reverse('ticket'))
        response = match.func(request)
        response.client = self.client
        self.assertRedirects(response, reverse('ticket_sent'))
        self.assertPostedToZendesk(mock_requests, {
            'subject': 'Test Feedback',
            'comment': {'body': 'The site is broken'},
            'tags': ['feedback', 'test'],
            'group_id': 222222,
            'requester_id': 111111,
            'custom_fields': [{'id': 32, 'value': 'Anonymous'},
                              {'id': 31, 'value': ''},
                              {'id': 33, 'value': 'test_client'}],
        })

    def test_submission_with_contact_email_shows_sent_page(self, mock_requests):
        response = self.client.post(reverse('ticket_with_email'), data={
            'ticket_content': 'Here is some feedback.\n  <script>alert("hello ");</script>  \n',
            'contact_email': 'example@example.com',
        }, HTTP_USER_AGENT='test_client2')
        self.assertRedirects(response, reverse('ticket_sent'))
        self.assertPostedToZendesk(mock_requests, {
            'subject': 'Test Feedback with email address',
            'comment': {'body': 'Here is some feedback.\n  <script>alert("hello ");</script>'},
            'tags': ['feedback', 'test', 'with-email'],
            'group_id': 222222,
            'requester': {'name': 'Sender: example',
                          'email': 'example@example.com'},
            'custom_fields': [{'id': 32, 'value': 'Anonymous'},
                              {'id': 34, 'value': 'example@example.com'},
                              {'id': 31, 'value': ''},
                              {'id': 33, 'value': 'test_client2'}],
        })

    def test_submission_provides_next_url_to_sent_page(self, mock_requests):
        response = self.client.post(reverse('ticket'), data={
            'referer': '/other/page',
            'ticket_content': 'The site is broken',
        }, HTTP_USER_AGENT='test_client')
        self.assertRedirects(response, '%s?next=/other/page' % reverse('ticket_sent'))
        self.assertPostedToZendesk(mock_requests, {
            'subject': 'Test Feedback',
            'comment': {'body': 'The site is broken'},
            'tags': ['feedback', 'test'],
            'group_id': 222222,
            'requester_id': 111111,
            'custom_fields': [{'id': 32, 'value': 'Anonymous'},
                              {'id': 31, 'value': '/other/page'},
                              {'id': 33, 'value': 'test_client'}],
        })

    @override_settings(ZENDESK_CUSTOM_FIELDS={})
    def test_custom_fields(self, mock_requests):
        response = self.client.post(reverse('ticket_with_email'), data={
            'referer': '/other/page',
            'ticket_content': 'The site is broken',
            'contact_email': 'example@example.com',
        }, HTTP_USER_AGENT='test_client')
        self.assertRedirects(response, '%s?next=/other/page' % reverse('ticket_sent'))
        self.assertPostedToZendesk(mock_requests, {
            'subject': 'Test Feedback with email address',
            'comment': {'body': 'The site is broken'},
            'tags': ['feedback', 'test', 'with-email'],
            'group_id': 222222,
            'requester': {'name': 'Sender: example',
                          'email': 'example@example.com'},
            'custom_fields': [],
        })


class TicketSentViewTestCase(SimpleTestCase):
    def test_next_url_provided(self):
        response = self.client.get(reverse('ticket_sent'), data={'next': '/another/page'})
        self.assertEqual(response.context['return_to'], '/another/page')

    def test_invalid_next_url_ignored(self):
        response = self.client.get(reverse('ticket_sent'), data={'next': 'http://phising-site.net/another/page'})
        self.assertIsNone(response.context['return_to'])
