import json

from django.conf import settings
import requests


TICKETS_URL = settings.ZENDESK_BASE_URL + '/api/v2/tickets.json'


def zendesk_auth():
    return (
        '{username}/token'.format(username=settings.ZENDESK_API_USERNAME),
        settings.ZENDESK_API_TOKEN
    )


def create_ticket(subject, tags, ticket_body, requester_email=None,
                  custom_fields=[]):
    """ Create a new Zendesk ticket """

    payload = {'ticket': {
        'subject': subject,
        'comment': {
            'body': ticket_body
        },
        'group_id': settings.ZENDESK_GROUP_ID,
        'tags': tags,
        'custom_fields': custom_fields
    }}

    if requester_email:
        payload['ticket']['requester'] = {
            'name': 'Sender: %s' % requester_email.split('@')[0],
            'email': requester_email,
        }
    else:
        payload['ticket']['requester_id'] = settings.ZENDESK_REQUESTER_ID

    requests.post(
        TICKETS_URL,
        data=json.dumps(payload),
        auth=zendesk_auth(),
        headers={'content-type': 'application/json'}).raise_for_status()
