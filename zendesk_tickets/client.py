import json

import requests
from django.conf import settings


TICKETS_URL = settings.ZENDESK_BASE_URL + '/api/v2/tickets.json'


def zendesk_auth():
    return (
        '{username}/token'.format(username=settings.ZENDESK_API_USERNAME),
        settings.ZENDESK_API_TOKEN
    )


def create_ticket(subject, tags, ticket_body, custom_fields=[]):
    """ Create a new Zendesk ticket """

    payload = {'ticket': {
        'requester_id': settings.ZENDESK_REQUESTER_ID,
        'subject': subject,
        'comment': {
            'body': ticket_body
        },
        'group_id': settings.ZENDESK_GROUP_ID,
        'tags': tags,
        'custom_fields': custom_fields
    }}

    return requests.post(
        TICKETS_URL,
        data=json.dumps(payload),
        auth=zendesk_auth(),
        headers={'content-type': 'application/json'})
