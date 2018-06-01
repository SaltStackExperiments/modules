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


def beacon(config):
    '''Check the RSS feed for changes'''
    list_of_dicts = []
    parsed_feed = feedparser.parse(config.get('url'))
    # Generate MD5 hash of the most current item's title and link elements.
    lasthash = __grains__.get('last_rss_hash')
    log.debug('{} parsed with {} entries'.format(
              config.get('url'), len(parsed_feed)))
    current_lasthash = hashlib.md5(parsed_feed.entries[0].link +
                                   parsed_feed.entries[0].title).hexdigest()


    log.debug('feed modified on %s', parsed_feed.modified)
    # Thu, 06 Mar 2014 00:13:50 GMT
    log.debug('current lasthash %s', current_lasthash)
    # 4167402f1ba2629fcc71003121aa1d25

    if lasthash != current_lasthash:
        # This rss feed has changed
        __salt__['grains.setval']('last_rss_hash', current_lasthash)
        _event = {
            'tag': 'my/beacons/rss/newentry',
            'entry': parsed_feed.entries[0]['link']
            }
        list_of_dicts.append(_event)
        log.debug('sending beacon event because there is a new rss entry')

    return list_of_dicts