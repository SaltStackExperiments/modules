# -*- coding: utf-8 -*-
import logging
import hashlib
import os

try:
    import feedparser
except:
    feedparser = None

__virtualname__ = 'rss'
log = logging.getLogger(__name__)
BASE = os.path.dirname(os.path.abspath(__file__))


def __virtual__():
    # Check required modules (aka feedparser in this case)
    if feedparser:
        log.debug('feedparser loaded')  # Thu, 06 Mar 2014 00:13:50 GMT
        return __virtualname__
    log.debug('feedparser not loaded')  # Thu, 06 Mar 2014 00:13:50 GMT
    return False


def validate(_config):
    print('config', _config, type(_config))
    valid_config = True
    comments = []
    # _config = {}
    # list(map(_config.update, config))

    if 'url' not in _config:
        comments.append('configuration for rss beacons must have a key "url"')
        valid_config = False

    for _url in _config.get('url'):
        if _url[:4] != 'http':
            comments.append(
                    '''configuration "url" must start with "http"
                    but it is {}'''.format(_url))
            valid_config = False
    return valid_config, comments


def beacon(config):
    '''Check the RSS feed for changes'''
    list_of_dicts = []
    url_list = config.get('url', [])
    if type(url_list) != list:
        url_list = []
        url_list.append(config.get('url', []))

    for _url in url_list:
        parsed_feed = feedparser.parse(_url)
        # Generate MD5 hash of the most current item's title and link elements.
        hash_key = 'last_rss_hash_{}'.format(_url)
        lasthash = __grains__.get(hash_key)
        log.debug('{} parsed with {} entries'.format(
                  config.get('url'), len(parsed_feed)))
        current_lasthash = hashlib.md5(_url + parsed_feed.entries[0].link +
                                       parsed_feed.entries[0].title
                                       ).hexdigest()
        log.debug('feed modified on %s', parsed_feed.modified)
        # Thu, 06 Mar 2014 00:13:50 GMT
        log.debug('current lasthash %s', current_lasthash)
        # 4167402f1ba2629fcc71003121aa1d25

        if lasthash != current_lasthash:
            # This rss feed has changed
            __salt__['grains.setval'](hash_key, current_lasthash)
            _event = {
                'tag': 'rss/{}/newentry'.format(_url),
                'rss_url': _url,
                'entry': parsed_feed.entries[0]['link']
                }
            list_of_dicts.append(_event)
            log.debug('sending beacon event because there is a new rss entry')

    return list_of_dicts
