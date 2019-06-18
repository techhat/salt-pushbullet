# -*- coding: utf-8 -*-
'''
Salt module for Pushbullet subscriptions
'''
# Import python libs
from __future__ import absolute_import
import json
import logging

# Import salt libs
import salt.utils.http

log = logging.getLogger(__name__)

__virtualname__ = 'pushbullet_subscriptions'
__func_alias__ = {
    'list_': 'list'
}


def __virtual__():
    '''
    Only load the module if Pushbullet is configured
    '''
    if 'access_token' in __opts__['pillar'].get('pushbullet', {}):
        return True
    return (False, 'The Pushbullet modules cannot be loaded: Pushbullet is not configured.')


def list_():
    '''
    List Pushbullet subscriptions

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_subscriptions.list
    '''
    url = 'https://api.pushbullet.com/v2/subscriptions'
    return salt.utils.http.query(
        url,
        header_dict={'Access-Token': __opts__['pillar']['pushbullet']['access_token']},
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']


def create(tag):
    '''
    Create a subscription

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_subscriptions.create elonmusknews
    '''
    api_url = 'https://api.pushbullet.com/v2/subscriptions'
    data = {'channel_tag': tag}

    res = salt.utils.http.query(
        api_url,
        method='POST',
        header_dict={'Access-Token': __opts__['pillar']['pushbullet']['access_token'],
                     'Content-Type': 'application/json'},
        opts=__opts__,
        data=json.dumps(data),
        decode=True,
        decode_type='json',
    )

    try:
        return res['dict']
    except KeyError:
        return res


def update(iden, muted):
    '''
    Update a subscription

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_subscriptions.update 0123456789abcdefghijkl true
    '''
    api_url = 'https://api.pushbullet.com/v2/subscriptions/{0}'.format(iden)
    data = {'muted': bool(muted)}

    res = salt.utils.http.query(
        api_url,
        method='POST',
        header_dict={'Access-Token': __opts__['pillar']['pushbullet']['access_token'],
                     'Content-Type': 'application/json'},
        opts=__opts__,
        data=json.dumps(data),
        decode=True,
        decode_type='json',
    )

    try:
        return res['dict']
    except KeyError:
        return res


def delete(iden):
    '''
    Delete a subscription

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_subscriptions.delete 0123456789abcdefghijkl
    '''
    api_url = 'https://api.pushbullet.com/v2/subscriptions/{0}'.format(iden)

    res = salt.utils.http.query(
        api_url,
        method='DELETE',
        header_dict={'Access-Token': __opts__['pillar']['pushbullet']['access_token'],
                     'Content-Type': 'application/json'},
        opts=__opts__,
        status=True,
        decode=True,
        decode_type='json',
    )

    if int(res.get('status', 0)) == 200:
        return True
    return False


def channel_info(tag, no_recent_pushes=False):
    '''
    Delete a subscription

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_subscriptions.channel_info elonmusknews
    '''
    api_url = 'https://api.pushbullet.com/v2/channel-info'
    data = {
        'tag': tag,
        'no-recent-pushes': no_recent_pushes,
    }

    res = salt.utils.http.query(
        api_url,
        method='GET',
        header_dict={'Access-Token': __opts__['pillar']['pushbullet']['access_token'],
                     'Content-Type': 'application/json'},
        opts=__opts__,
        params=data,
        decode=True,
        decode_type='json',
    )

    try:
        return res['dict']
    except KeyError:
        return res
