# -*- coding: utf-8 -*-
'''
Salt module for Pushbullet chats
'''
# Import python libs
from __future__ import absolute_import
import json
import logging

# Import salt libs
import salt.utils.http

log = logging.getLogger(__name__)

__virtualname__ = 'pushbullet_chats'
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
    List Pushbullet chats

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_chats.list
    '''
    url = 'https://api.pushbullet.com/v2/chats'
    return salt.utils.http.query(
        url,
        header_dict={'Access-Token': __opts__['pillar']['pushbullet']['access_token']},
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']


def create(email):
    '''
    Create a chat

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_chats.create
    '''
    api_url = 'https://api.pushbullet.com/v2/chats'
    data = {'email': email}

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
    Update a chat

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_chats.update 0123456789abcdefghijkl true
    '''
    api_url = 'https://api.pushbullet.com/v2/chats/{0}'.format(iden)
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
    Delete a chat

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_chats.delete 0123456789abcdefghijkl
    '''
    api_url = 'https://api.pushbullet.com/v2/chats/{0}'.format(iden)

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
