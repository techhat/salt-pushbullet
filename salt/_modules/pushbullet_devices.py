# -*- coding: utf-8 -*-
'''
Salt module for Pushbullet devices
'''
# Import python libs
from __future__ import absolute_import
import json
import logging

# Import salt libs
import salt.utils.http

log = logging.getLogger(__name__)

__virtualname__ = 'pushbullet_devices'
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
    List Pushbullet devices

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_devices.list
    '''
    url = 'https://api.pushbullet.com/v2/devices'
    return salt.utils.http.query(
        url,
        header_dict={'Access-Token': __opts__['pillar']['pushbullet']['access_token']},
        opts=__opts__,
        decode=True,
        decode_type='json',
    )['dict']


def create(
        nickname=None,
        model=None,
        manufacturer=None,
        push_token=None,
        app_version=None,
        icon=None,
        has_sms=None,
    ):
    '''
    Create a device

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_devices.create
    '''
    api_url = 'https://api.pushbullet.com/v2/devices'
    data = {}

    if nickname is not None:
        data['nickname'] = nickname

    if model is not None:
        data['model'] = model

    if manufacturer is not None:
        data['manufacturer'] = manufacturer

    if push_token is not None:
        data['push_token'] = push_token

    if app_version is not None:
        data['app_version'] = app_version

    if icon is not None:
        data['icon'] = icon

    if has_sms is not None:
        data['has_sms'] = has_sms

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
    Update a device

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_devices.update 0123456789abcdefghijkl true
    '''
    api_url = 'https://api.pushbullet.com/v2/devices/{0}'.format(iden)
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
    Delete a device

    CLI Example:

    .. code-block:: bash

        salt minion pushbullet_devices.delete 0123456789abcdefghijkl
    '''
    api_url = 'https://api.pushbullet.com/v2/devices/{0}'.format(iden)

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
