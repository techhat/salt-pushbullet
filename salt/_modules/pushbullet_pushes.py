# -*- coding: utf-8 -*-
'''
Salt module for Pushbullet pushes
'''
# Import python libs
from __future__ import absolute_import
import json
import logging

# Import salt libs
import salt.utils.http

log = logging.getLogger(__name__)

__virtualname__ = 'pushbullet_pushes'
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
    List Pushbullet pushes

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_pushes.list
    '''
    url = 'https://api.pushbullet.com/v2/pushes'
    return salt.utils.http.query(
        url,
        header_dict={'Access-Token': __opts__['pillar']['pushbullet']['access_token']},
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']


def create(
        device,
        type_,
        body,
        title=None,
        url=None,
        file_name=None,
        file_type=None,
        file_url=None,
    ):
    '''
    Create a push

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_pushes.create
    '''
    api_url = 'https://api.pushbullet.com/v2/pushes'
    data = {
        'device_iden': device,
        'type': type_,
        'body': body,
    }

    if title is not None:
        data['title'] = title

    if url is not None:
        data['url'] = url

    if file_name is not None:
        data['file_name'] = file_name

    if file_type is not None:
        data['file_type'] = file_type

    if file_url is not None:
        data['file_url'] = file_url

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


def update(iden, dismissed):
    '''
    Update a push

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_pushes.update 0123456789abcdefghijkl true
    '''
    api_url = 'https://api.pushbullet.com/v2/pushes/{0}'.format(iden)
    data = {'dismissed': bool(dismissed)}

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
    Delete a push

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_pushes.delete 0123456789abcdefghijkl
    '''
    api_url = 'https://api.pushbullet.com/v2/pushes/{0}'.format(iden)

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


def delete_all():
    '''
    Delete all pushes

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_pushes.delete_all
    '''
    api_url = 'https://api.pushbullet.com/v2/pushes'

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
